# Imports
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



# Functions
def startSumo(gui=True):
    sumoBinary = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo-gui.exe"
    sumoCmd = [sumoBinary, "-c", "Configuration.sumocfg", "--start"]
    traci.start(sumoCmd)
   
def stopSumo():
    traci.close()




# Parameters
vehicle_spawn_period = 10
simulation_duration = 1000 # seconds
free_flow_speed = 13.89
grid_resolution_x = 10.0 # m
grid_resolution_t = 10.0 # s
heatmap_frame_border = 5


# Start Sumo
startSumo()
print("Started SUMO")

# Initialize simulation recording data
    # Time Space Information
vehicle_data = []
times_yet = [traci.simulation.getTime()]
positions_yet = [0]
lane_ids = list(traci.lane.getIDList())
print("Initialization Finished")

# Run Simulation
print("Start Simulation")
last_vehicle_spawn_time = 0
vehicle_spawn_iteration = 1
traci.vehicle.add(vehID="v_0", routeID="r_0")
while traci.simulation.getTime()<=simulation_duration+1:
    if traci.simulation.getTime() - last_vehicle_spawn_time > vehicle_spawn_period:
        last_vehicle_spawn_time = traci.simulation.getTime()
        traci.vehicle.add(vehID="v_"+str(vehicle_spawn_iteration), routeID="r_0")
        vehicle_spawn_iteration += 1
    traci.simulationStep()
    # retrieve vehicle data
    vehicle_ids = list(traci.vehicle.getIDList())
    vehicle_lanes = [traci.vehicle.getLaneID(vehicle_id) for vehicle_id in vehicle_ids]
    vehicle_positions = [traci.vehicle.getDistance(vehicle_id) for vehicle_id in vehicle_ids]
    vehicle_speeds = [traci.vehicle.getSpeed(vehicle_id) for vehicle_id in vehicle_ids]
    # Record Time Space Diagram
    for key in vehicle_ids:
        position_x = traci.vehicle.getPosition(key)[0]
        position_dx = round(position_x / grid_resolution_x) * grid_resolution_x
        position_time = traci.simulation.getTime()
        discrete_time = round(position_time / grid_resolution_t) * grid_resolution_t
        vehicle_data.append([position_time, discrete_time, traci.vehicle.getSpeed(key), position_x, position_dx])
print("Simulation Finished")

# Stop Sumo
stopSumo()
print("Closed SUMO")



# Process Recordings
vehicle_data = pd.DataFrame(vehicle_data, columns=["position_time", "disc_time", "speed", "position_x", "disc_x"])
vehicle_data = vehicle_data.groupby(["disc_time", "disc_x"]).mean()
del vehicle_data["position_x"]
del vehicle_data["position_time"]
vehicle_data.reset_index(inplace=True)


# Display Heatmap
minx = min(vehicle_data["disc_x"])
maxx = max(vehicle_data["disc_x"])
miny = min(vehicle_data["disc_time"])
maxy = max(vehicle_data["disc_time"])
new_row_top_left = pd.DataFrame([[minx-heatmap_frame_border, miny-heatmap_frame_border, free_flow_speed]], columns=vehicle_data.columns)
new_row_bot_righ = pd.DataFrame([[maxx+heatmap_frame_border, maxy+heatmap_frame_border, free_flow_speed]], columns=vehicle_data.columns)
vehicle_data_border = pd.concat([vehicle_data, new_row_top_left, new_row_bot_righ], ignore_index=True)
heatmap_data = vehicle_data_border.pivot(index='disc_x', columns='disc_time', values='speed')
heatmap_data.fillna(free_flow_speed, inplace=True)

fig = plt.figure("Time Space Heatmap", figsize=(15, 5))
im = plt.gca().imshow(np.asarray(heatmap_data)[:, ::-1][::-1], origin='lower', aspect='auto', extent=[0, heatmap_data.shape[1], 0, heatmap_data.shape[0]])
cbar = plt.colorbar(im)
cbar.set_label('Speed [m/s]', rotation=270, labelpad=15)
plt.xlabel("Time")
plt.ylabel("Space")
plt.tight_layout()

