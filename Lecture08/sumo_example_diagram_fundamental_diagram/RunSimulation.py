# Imports
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import numpy as np




# Functions
def startSumo(sumoBinary, sumoConfigFile):
    sumoCmd = [sumoBinary, "-c", sumoConfigFile, "--start"]
    traci.start(sumoCmd)
   
def stopSumo():
    traci.close()




# Parameters
sumo_location = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo.exe"
simulation_config_file = "Configuration.sumocfg" 
simulation_steady_state_iterations = 100 # seconds
flow_observation_period = 2000 # seconds




# Start Sumo
startSumo(sumo_location, simulation_config_file)
print("Started SUMO")

# Prepare MFD recorder
mfd_record = []
excluded_lanes = [
    "E0", "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12","E13","E14","E15","E16","E17","E18","E19",
    "-E0","-E1","-E2","-E3","-E4","-E5","-E6","-E7","-E8","-E9","-E10","-E11","-E12","-E13","-E14","-E15","-E16","-E17","-E18","-E19", 
    ]
total_length = 0
for lane in traci.lane.getIDList():
    if lane not in excluded_lanes:
        total_length += traci.lane.getLength(lane)

# Warmup Simulation
for it in range(0,simulation_steady_state_iterations):
    traci.simulationStep()


# Run Simulation until no vehicles left
print("Simulation Started")
while traci.simulation.getTime()<flow_observation_period:
    # Record MFD
    # speeds = []
    lanespeeds = []
    lanedensities = []
    waitingtimes = []
    # num_vehicles = []
    for lane in traci.lane.getIDList():
        if (lane[-2] not in excluded_lanes) and (not lane.startswith(":")):
            lanespeeds.append(traci.lane.getLastStepMeanSpeed(lane))
            lanedensities.append(traci.lane.getLastStepVehicleNumber(lane)/traci.lane.getLength(lane))
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for vid in vehicles:
                waitingtimes.append(traci.vehicle.getWaitingTime(vid))
    density = np.average(lanedensities) 
    velocity = np.average(lanespeeds) 
    waitingtime = np.average(waitingtimes)
    flow = density*velocity
    mfd_record.append([traci.simulation.getTime(), density, velocity, flow, waitingtime])
    # Exit Simulation
    if not (traci.vehicle.getIDCount() > 0):
        break
    # Continue Simulation
    traci.simulationStep()
    print(traci.simulation.getTime(), "/", flow_observation_period)
    
    
print("Simulation Finished")
mfd_record = np.asarray(mfd_record)

stopSumo()
print("Closed SUMO")
    



# Draw Results
import matplotlib.pyplot as plt
    # Draw Fundamental Diagram
plt.figure("Macroscopic Fundamental Diagram", figsize=(15,5))
plt.suptitle("Macroscopic Fundamental Diagram]")
plt.subplot(1,4,1)
plt.xlabel("k [v/m]")
plt.ylabel("q [v/s]")
plt.scatter(mfd_record[:,1], mfd_record[:,3])
plt.gca().set_ylim(bottom=0)
plt.subplot(1,4,2)
plt.xlabel("k [v/m]")
plt.ylabel("v [m/s]")
plt.scatter(mfd_record[:,1], mfd_record[:,2])
plt.gca().set_ylim(bottom=0)
plt.subplot(1,4,3)
plt.xlabel("q [v/s]")
plt.ylabel("v [m/s]")
plt.scatter(mfd_record[:,3], mfd_record[:,2])
plt.gca().set_ylim(bottom=0)
plt.subplot(1,4,4)
plt.xlabel("Time [s]")
plt.ylabel("Average waiting time [s]")
plt.plot(mfd_record[:,0], mfd_record[:,4])
plt.tight_layout()