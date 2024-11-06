# IMPORTS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# PARAMETERS
file = "../simulation_output/scenario_1_model/log_emissions.xml"
scenario = "Scenario 1 - Emissions Heatmap"
grid_resolution = 5.0 # m
heatmap_frame_border = 2



# METHODS FOR LOADING
def loadTimeStepLogs(file):
    file_reader = open(file, "r")
    file_content = file_reader.read()
    file_reader.close()
    parts = file_content.split("<timestep time=\"")[1:]
    return parts

def extractInformationFromParts(parts):
    emission_info = []
    for part in parts:
        time = float(part.split("\"")[0])
        vehicle_parts = part.split("<vehicle id=")[1:]
        for vehicle_part in vehicle_parts:
            veh_pos_x  = float(vehicle_part.split(" x=\"")[1].split("\"")[0])
            veh_pos_y  = float(vehicle_part.split(" y=\"")[1].split("\"")[0])
            veh_em_co2 = float(vehicle_part.split(" CO2=\"")[1].split("\"")[0])
            veh_em_co  = float(vehicle_part.split(" CO=\"")[1].split("\"")[0])
            veh_em_nox = float(vehicle_part.split(" NOx=\"")[1].split("\"")[0])
            veh_em_pmx = float(vehicle_part.split(" PMx=\"")[1].split("\"")[0])
            veh_em_noise = float(vehicle_part.split(" noise=\"")[1].split("\"")[0])
            emission_info.append([
                    time,
                    veh_pos_x,
                    veh_pos_y,
                    veh_em_co2,
                    veh_em_co,
                    veh_em_nox,
                    veh_em_pmx,
                    veh_em_noise
                ])
    return emission_info

def addSpatialDiscretization(emission_info, grid_resolution):
    emission_info_modified = []
    for info in emission_info:
        veh_pos_x = info[1]
        veh_pos_y = info[2]
        discretized_x, discretized_y = discretize_position(veh_pos_x, veh_pos_y, grid_resolution)
        emission_info_modified.append([discretized_x, discretized_y, *info])
    return emission_info_modified

def discretize_position(x, y, grid_resolution):
    discretized_x = round(x / grid_resolution) * grid_resolution
    discretized_y = round(y / grid_resolution) * grid_resolution
    return discretized_x, discretized_y




# MAIN CODE
    # Read From File
content_parts = loadTimeStepLogs(file)
emission_info = extractInformationFromParts(content_parts)
emission_info = addSpatialDiscretization(emission_info, grid_resolution)
emission_info = pd.DataFrame(emission_info, columns=["grid_x", "grid_y", "time", "pos_x", "pos_y", "em_co2", "em_co", "em_nox", "em_pmx", "em_pmx" ])
    # Aggregate over time
emission_info_agg = emission_info.groupby(["grid_x", "grid_y"]).sum()
del emission_info_agg["pos_x"]
del emission_info_agg["pos_y"]
del emission_info_agg["time"]
emission_info_agg.reset_index(inplace=True)
minx = min(emission_info_agg["grid_x"])
maxx = max(emission_info_agg["grid_x"])
miny = min(emission_info_agg["grid_y"])
maxy = max(emission_info_agg["grid_y"])
new_row_top_left = pd.DataFrame([[minx-heatmap_frame_border, miny-heatmap_frame_border, 0, 0, 0, 0, 0]], columns=emission_info_agg.columns)
new_row_bot_righ = pd.DataFrame([[maxx+heatmap_frame_border, maxy+heatmap_frame_border, 0, 0, 0, 0, 0]], columns=emission_info_agg.columns)
emission_info_agg_border = pd.concat([emission_info_agg, new_row_top_left, new_row_bot_righ], ignore_index=True)
    # Display Heatmap
plt.figure(figsize=(15,10))
plt.suptitle(scenario)
plt.subplot(1,3,1)
plt.title("CO_2 Emissions")
heatmap_data = emission_info_agg_border.pivot(index='grid_x', columns='grid_y', values='em_co2')
heatmap_data.fillna(0, inplace=True)
im = plt.imshow(np.asarray(heatmap_data)[:, ::-1][::-1], origin='lower')
cbar = plt.gcf().colorbar(im, ax=plt.gca(), orientation='horizontal', pad=0.1)
cbar.set_label('CO_2')
plt.subplot(1,3,2)
plt.title("CO Emissions")
heatmap_data = emission_info_agg_border.pivot(index='grid_x', columns='grid_y', values='em_co')
heatmap_data.fillna(0, inplace=True)
im = plt.imshow(np.asarray(heatmap_data)[:, ::-1][::-1], origin='lower')
cbar = plt.gcf().colorbar(im, ax=plt.gca(), orientation='horizontal', pad=0.1)
cbar.set_label('CO')
plt.subplot(1,3,3)
plt.title("NOX Emissions")
heatmap_data = emission_info_agg_border.pivot(index='grid_x', columns='grid_y', values='em_nox')
heatmap_data.fillna(0, inplace=True)
im = plt.imshow(np.asarray(heatmap_data)[:, ::-1][::-1], origin='lower')
cbar = plt.gcf().colorbar(im, ax=plt.gca(), orientation='horizontal', pad=0.1)
cbar.set_label('NOX')
plt.tight_layout()