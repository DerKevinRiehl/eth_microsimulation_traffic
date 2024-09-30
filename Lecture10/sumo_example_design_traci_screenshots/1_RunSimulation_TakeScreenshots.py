# PYTHON IMPORTS
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import time

# METHODS
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")



# START SUMO
sumoBinary = "C:/Users/kriehl/AppData/Local/sumo-1.19.0/bin/sumo-gui.exe"
sumoConfigFile = "Configuration.sumocfg" 
screenshot_folder = "screenshots"
sumoCmd = [sumoBinary, "-c", sumoConfigFile, "--start", "--quit-on-end", "--time-to-teleport", "-1"]
traci.start(sumoCmd)
create_folder_if_not_exists(screenshot_folder)


# Set Specific Position
traci.simulationStep()
traci.gui.setOffset("View #0", 100, 100) # focus on middle intersection
traci.gui.setZoom("View #0", 200)        # double size
traci.gui.setAngle("View #0", 45)        # angle in degree
traci.simulationStep()
traci.gui.screenshot("View #0", screenshot_folder+"/Screenshot_"+"{0:0=3d}".format(0)+".png")
traci.simulationStep()


# RUN SIMULATION
for it in range(1, 500):
    traci.gui.setZoom("View #0", 100+it)
    traci.gui.setAngle("View #0", it)
    traci.gui.screenshot("View #0", screenshot_folder+"/Screenshot_"+"{0:0=3d}".format(it)+".png")
    traci.simulationStep()


# STOP SUMO
traci.close()
