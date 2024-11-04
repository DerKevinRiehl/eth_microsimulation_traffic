# #############################################################################
# IMPORTS
# #############################################################################
import numpy as np
import pandas as pd


# #############################################################################
# METHODS
# #############################################################################


SAMPLING_FREQ_SUMO_LANE_DATA = 300

# #############################################################################
# MAIN CODE
# #############################################################################

# Load File
# f = open("../simulation_output/scenario_1_model/log_edge_data.xml", "r", encoding="utf-8")
f = open("../simulation_models/scenario_2_model/log_edge_data.xml", "r", encoding="utf-8")
content = f.read()
f.close()

# Process Lines
lines = content.split("-->")[1].split("\n")[3:]
lines = [line.strip() for line in lines]

# Analyse Each Timesteps
timesteps = []
for line in lines:
    if line.startswith("<interval"):
        timestep = line.split("begin=\"")[1].split("\"")[0]
        if timestep not in timesteps:
            timesteps.append(timestep)
            
# Analyse Each Edges
edges = []
for line in lines:
    if line.startswith("<edge"):
        edge = line.split("id=\"")[1].split("\"")[0]
        if edge not in edges:
            edges.append(edge)
n_edges = len(edges)

# Calculate MDF
mfd_data = []
ctr = 0
curr_time = 0
lst_densities = []
lst_speeds = []
lst_num_veh_left = []

last_densities = {}
for edge in edges:
    last_densities[edge] = 0

while ctr<len(lines):
    line = lines[ctr]
    if line.startswith("<interval"):
        curr_time = line.split("begin=\"")[1].split("\"")[0]
        lst_densities = []
        lst_flows = []
        lst_speeds = []
        lst_num_veh_left = []
    elif line.startswith("</interval"):
        n_edges = len(lst_densities)
        row = [curr_time, 
               np.sum(lst_densities)/n_edges, # veh/km
               np.sum(lst_speeds)/n_edges * 3.6, # km/h
               np.sum(lst_num_veh_left)/n_edges / SAMPLING_FREQ_SUMO_LANE_DATA * 3600, # veh/h
               ]
        mfd_data.append(row)
    elif line.startswith("<edge"):
        if "traveltime=\"" in line:
            lst_densities.append(float(line.split("density=\"")[1].split("\"")[0]))
            lst_speeds.append(float(line.split("speed=\"")[1].split("\"")[0]))
            lst_num_veh_left.append(float(line.split("left=\"")[1].split("\"")[0]))
            edge_id = line.split("id=\"")[1].split("\"")[0]
            last_densities[edge_id] = float(line.split("density=\"")[1].split("\"")[0])
        else:
            edge_id = line.split("id=\"")[1].split("\"")[0]
            lst_densities.append(last_densities[edge_id])
            lst_speeds.append(0)
            lst_num_veh_left.append(0)

    ctr += 1
df_mfd = pd.DataFrame(mfd_data, columns=["time", "density", "speed", "flow"])

import matplotlib.pyplot as plt
# plt.scatter(df_mfd["density"], df_mfd["flow"])
plt.scatter(df_mfd["density"], df_mfd["speed"])
plt.ylim(0, 35)