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

input()

# RUN SIMULATION
for it in range(0, 500):
    traci.simulationStep()
    time.sleep(0.1)
    
# STOP SUMO
traci.close()

