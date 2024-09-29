# PYTHON IMPORTS
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import time

# START SUMO
sumoBinary = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo-gui.exe"
sumoConfigFile = "Configuration.sumocfg" 
sumoCmd = [sumoBinary, "-c", sumoConfigFile, "--start", "--quit-on-end", "--time-to-teleport", "-1"]
traci.start(sumoCmd)

# RUN SIMULATION A
for it in range(0, 500):
    traci.simulationStep()
    time.sleep(0)
    
# GET INFO ABOUT VEHICLES
lst_vehicles = traci.vehicle.getIDList()
    # ('f_0.0', 'f_0.1', 'f_0.2', 'f_0.3', 'f_0.4')
for veh_id in lst_vehicles:
    veh_position = traci.vehicle.getPosition(veh_id)
        # (1.6, 154.6488693732702)
    veh_speed = traci.vehicle.getSpeed(veh_id)
         # 14.222625294149202
    veh_acceleration = traci.vehicle.getAcceleration(veh_id)
         # -0.6609447418712122 
    print(veh_id)
    print("\t", veh_position, "\n\t", veh_speed, "\n\t", veh_acceleration, "\n")
    
# GET INFO ABOUT EDGES (ROADS)
lst_edges = traci.edge.getIDList()
edge_id = "E6"
#for edge_id in lst_edges:
num_vehicles = traci.edge.getLastStepVehicleNumber(edge_id)
mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)
occupancy = traci.edge.getLastStepOccupancy(edge_id)
fuel_consumption = traci.edge.getFuelConsumption(edge_id)
print(edge_id)
print("\t", num_vehicles, "\n\t", mean_speed, "\n\t", occupancy, "\n\t", fuel_consumption, "\n")

# RUN SIMULATION B
for it in range(0, 500):
    traci.simulationStep()
    time.sleep(0)
        
# STOP SUMO
traci.close()

