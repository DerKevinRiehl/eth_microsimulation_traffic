# Imports
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import numpy as np

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


# Car following model by Wiedemann, 10-Parameter version
# https://w99demo.com/

def runSimulation(x=5):
    # Start Sumo
    startSumo()
    route1 = "0_0"
    route2 = "1_0"
    route3 = "2_0"
    route4 = "3_0"
    
    for n in range(0, x+1):
        traci.vehicle.add("v"+str(n), str(n)+"_0", typeID="vtype1")
        
    # Warmup Run
    for it in range(0, 400):
        traci.simulationStep()
        
    # Run For Recording
    vehicle_t = {}
    vehicle_s = {}
    vehicle_v = {}
    times_yet = [traci.simulation.getTime()]
    positions_yet = [0]
    for it in range(0, 300):
        traci.simulationStep()
        # Record Time Space Diagram
        vehicle_ids = list(traci.vehicle.getIDList())
        vehicle_lanes = [traci.vehicle.getLaneID(vehicle_id) for vehicle_id in vehicle_ids]
        vehicle_positions = [traci.vehicle.getDistance(vehicle_id) for vehicle_id in vehicle_ids]
        vehicle_speeds = [traci.vehicle.getSpeed(vehicle_id) for vehicle_id in vehicle_ids]
        
        for key in vehicle_ids:
            if key not in vehicle_t:
                vehicle_t[key] = times_yet.copy()
                vehicle_s[key] = positions_yet.copy()
                vehicle_v[key] = positions_yet.copy()
            vehicle_t[key].append(traci.simulation.getTime())
            vehicle_s[key].append(vehicle_positions[vehicle_ids.index(key)])   
            vehicle_v[key].append(vehicle_speeds[vehicle_ids.index(key)])
        for key in vehicle_t:
            if key not in vehicle_ids:
                vehicle_t[key].append(traci.simulation.getTime())
                vehicle_s[key].append(vehicle_s[key][-1])     
                vehicle_v[key].append(vehicle_v[key][-1])     
        times_yet.append(traci.simulation.getTime())
        positions_yet.append(0)
        
    # # Stop Sumo
    stopSumo()

    return vehicle_t, vehicle_s, vehicle_v


# Draw Results
import matplotlib.pyplot as plt
    # Draw Time Space Diagram
plt.figure("Raum-Zeit-Diagramm", figsize=(8,8))


vehicle_t, vehicle_s, vehicle_v = runSimulation(x=5)

plt.subplot(2,2,1)

plt.suptitle("Fahrzeug-Abstand-Modell nach Wiedemann (10-Parameter version)", fontweight="bold")

plt.title("Raum-Zeit-Diagramm (5 Fahrzeuge)")
plt.ylabel("Position [m]")
plt.xlabel("Zeit [s]")
# plt.ylim([350,550])

plt.ylim([5000, 5600])
plt.xlim([450,490])

diameter = 2*3.1415*radius
for key in vehicle_t:
    plt.plot(vehicle_t[key], vehicle_s[key], color=(0,0,1/len(vehicle_t)*int(key[1:])))

plt.subplot(2,2,2)
plt.title("Geschwindigkeit-Zeit-Diagramm")
plt.ylabel("Geschwindigkeit [kmh]")
plt.xlabel("Zeit [s]")
average = []
for key in vehicle_t:
    plt.plot(vehicle_t[key], np.asarray(vehicle_v[key])*3.6, color=(0,0,1/len(vehicle_t)*int(key[1:])), alpha=0.05)
    average.append(vehicle_v[key])
average = np.asarray(average)
stds = np.std(average, axis=0)
average = np.mean(average, axis=0)
# plt.plot(vehicle_t[key], np.asarray(vehicle_v[key])*3.6, color="black")
plt.plot(vehicle_t[key], average*3.6, color="black")
plt.plot(vehicle_t[key], average*3.6+stds, "--", color="black")
plt.plot(vehicle_t[key], average*3.6-stds, "--", color="black")
plt.xlim([450,490])


vehicle_t, vehicle_s, vehicle_v = runSimulation(x=10)

plt.subplot(2,2,3)
plt.title("Raum-Zeit-Diagramm (10 Fahrzeuge)")
plt.ylabel("Position [m]")
plt.xlabel("Zeit [s]")
# plt.ylim([350,550])

plt.ylim([1825, 2050])
plt.xlim([450,490])

diameter = 2*3.1415*radius
for key in vehicle_t:
    plt.plot(vehicle_t[key], vehicle_s[key], color=(0,0,1/len(vehicle_t)*int(key[1:])))

plt.subplot(2,2,4)
plt.title("Geschwindigkeit-Zeit-Diagramm")
plt.ylabel("Geschwindigkeit [kmh]")
plt.xlabel("Zeit [s]")
average = []
for key in vehicle_t:
    plt.plot(vehicle_t[key], np.asarray(vehicle_v[key])*3.6, color=(0,0,1/len(vehicle_t)*int(key[1:])), alpha=0.05)
    average.append(vehicle_v[key])
average = np.asarray(average)
stds = np.std(average, axis=0)
average = np.mean(average, axis=0)
# plt.plot(vehicle_t[key], np.asarray(vehicle_v[key])*3.6, color="black")
plt.plot(vehicle_t[key], average*3.6, color="black")
plt.plot(vehicle_t[key], average*3.6+stds, "--", color="black")
plt.plot(vehicle_t[key], average*3.6-stds, "--", color="black")
plt.xlim([450,490])


plt.tight_layout()