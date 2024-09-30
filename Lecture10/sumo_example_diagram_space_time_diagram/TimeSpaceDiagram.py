# Imports
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec



# Functions
def startSumo(gui=True):
    sumoBinary = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo-gui.exe"
    sumoCmd = [sumoBinary, "-c", "Configuration.sumocfg", "--start"]
    traci.start(sumoCmd)
   
def stopSumo():
    traci.close()




# Parameters
vehicle_spawn_period = 10
simulation_duration = 500 # seconds
free_flow_speed = 13.89




# Start Sumo
startSumo()
print("Started SUMO")

# Initialize simulation recording data
    # Time Space Information
vehicle_t = {}
vehicle_s = {}
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
        if key not in vehicle_t:
            vehicle_t[key] = times_yet.copy()
            vehicle_s[key] = positions_yet.copy()
        vehicle_t[key].append(traci.simulation.getTime())
        vehicle_s[key].append(vehicle_positions[vehicle_ids.index(key)])      
    for key in vehicle_t:
        if key not in vehicle_ids:
            vehicle_t[key].append(traci.simulation.getTime())
            vehicle_s[key].append(vehicle_s[key][-1])     
    times_yet.append(traci.simulation.getTime())
    positions_yet.append(0)
print("Simulation Finished")

# Stop Sumo
stopSumo()
print("Closed SUMO")





# Draw Results
fig = plt.figure("Time Space Diagram", figsize=(15, 7))
gs = GridSpec(2, 2, width_ratios=[20, 1], height_ratios=[1, 1])

# Upper subplot
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title("Time Space Diagram")
ax1.set_ylabel("Position [m]")
ax1.set_xlabel("Time [s]")
ax1.set_ylim([0, 350])
ax1.set_xlim([0, 500])
for key in vehicle_t:
    ax1.plot(vehicle_t[key], vehicle_s[key], color="black")

# Lower subplot
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_title("Time Space Diagram (Speed = Color)")
ax2.set_ylabel("Position [m]")
ax2.set_xlabel("Time [s]")
ax2.set_ylim([0, 350])
ax2.set_xlim([0, 500])

# Plot colored lines in lower subplot
for key in vehicle_t:
    x = vehicle_t[key]
    y = vehicle_s[key]
    slope = np.gradient(y, x)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(slope.min(), slope.max())
    lc = LineCollection(segments, cmap='coolwarm', norm=norm)
    lc.set_array(slope)
    ax2.add_collection(lc)

# Add colorbar to lower subplot
cbar_ax = fig.add_subplot(gs[1, 1])
plt.colorbar(lc, cax=cbar_ax, label='Slope')

# Adjust layout
plt.tight_layout()
plt.show()
