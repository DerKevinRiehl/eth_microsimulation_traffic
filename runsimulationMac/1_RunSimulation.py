# Imports
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import numpy as np
import time




# Functions
def startSumo():
    sumoBinary = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo-gui.exe"
    sumoConfigFile = "SumoSimulation/Configuration.sumocfg" #"Configuration.sumocfg"
    sumoCmd = [sumoBinary, "-c", sumoConfigFile, "--start", "--quit-on-end", "--time-to-teleport", "-1"]
    traci.start(sumoCmd)
   
def stopSumo():
    traci.close()

def spawnProcedure(route, flow_third, vcounter):
    spawn_prob = flow_third/60/60

    rand_exp_variable = min(1, np.random.exponential(1/5))
    if rand_exp_variable <= -np.log(1-spawn_prob)/5: # CDF of exp. variable CDF(x) = 1-e^(-lambda*x)
        traci.vehicle.add("v"+str(vcounter)+"_2", route)
        vcounter += 1

    return vcounter

# Parameters
fundamental_diagram_lane_name = "E0_0" #'E0_0'
vehicle_spawn_period = 5
simulation_steady_state_iterations = 100
flow_observation_period = 2000 # seconds
vehicles_per_spawn = 3
radius = 27.3


# Freeflow Speeds
# RouteA = 138s [0]
# routeA_1 = 138s [0]
# routeA_2 = 139s [0]
# routeA_3 = 138s [0]
# 0 149.74358974358975 147.0 156 [ 10.365049627493715 ]
# 100 152.63276836158192 151.0 177 [ 10.99489607926338 ]
# 200 154.9047619047619 154.0 189 [ 10.518888456548062 ]
# 300 158.35 158.0 200 [ 9.655438881790927 ]
# 400 164.605 162.0 200 [ 11.037163358399658 ]

# RouteB = 241s
# routeB_1 = 241s [0]
# routeB_2 = 240s [0]
# routeB_3 = 241s [0]
# 0 264.18589743589746 258.5 156 [ 19.279258313474763 ]
# 100 265.85185185185185 265.0 162 [ 21.044110704329533 ]
# 200 267.42011834319527 265.0 169 [ 22.705885324918775 ]
# 300 267.2471264367816 264.0 174 [ 20.78466133751157 ]
# 400 269.95628415300547 267.0 183 [ 20.322757745132535 ]


# Start Sumo
startSumo()
route1 = "0_0"
route2 = "1_0"
route3 = "2_0"
route4 = "3_0"

traci.vehicle.add("v0", "0_0", typeID="vtype1")
traci.vehicle.add("v1", "1_0", typeID="vtype1")
traci.vehicle.add("v3", "2_0", typeID="vtype1")
traci.vehicle.add("v4", "3_0", typeID="vtype1")
traci.vehicle.add("v5", "4_0", typeID="vtype1")
traci.vehicle.add("v6", "5_0", typeID="vtype1")
traci.vehicle.add("v7", "6_0", typeID="vtype1")
traci.vehicle.add("v8", "7_0", typeID="vtype1")
traci.vehicle.add("v9", "8_0", typeID="vtype1")
traci.vehicle.add("v10", "9_0", typeID="vtype1")
traci.vehicle.add("v11", "10_0", typeID="vtype1")
traci.vehicle.add("v12", "11_0", typeID="vtype1")
traci.vehicle.add("v13", "12_0", typeID="vtype1")
traci.vehicle.add("v14", "13_0", typeID="vtype1")
traci.vehicle.add("v15", "14_0", typeID="vtype1")
    

# Warmup Run
for it in range(0, 1000):
    traci.simulationStep()
    time.sleep(0.1)
    