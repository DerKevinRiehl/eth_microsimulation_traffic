# IMPORTS
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline




# PARAMETERS
path_to_results_scenario_1 = "../simulation_output/scenario_1_model/"
path_to_results_scenario_2 = "../simulation_output/scenario_2_model/"
path_to_results_scenario_3 = "../simulation_output/scenario_3_model/"





# Methods
def doPolynomialModel(df, xlab, ylab):
    poly_reg = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    X = df[xlab].values.reshape(-1, 1)
    y = df[ylab].values
    poly_reg.fit(X, y)
    x_smooth = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
    y_smooth = poly_reg.predict(x_smooth)
    return [x_smooth, y_smooth]
    
def loadMFD(path_to_results):
    # determine relevant files
    files = os.listdir(path_to_results)
    sensors = [file for file in files if file.startswith("e")]
    sensor_data = {
    }
    # extract sensor information
    for sensor in sensors:
        f = open(path_to_results+sensor, "r")
        content = f.read()
        f.close()
        lines = content.split("\n")
        lines = [line.strip() for line in lines]
        for line in lines:
            if line.startswith("<interval"):
                time = float(line.split("begin=")[1].split("\"")[1])
                flow = float(line.split("flow=")[1].split("\"")[1])
                speed = float(line.split("speed=")[1].split("\"")[1])
                occupancy = float(line.split("occupancy=")[1].split("\"")[1])
                if speed!=-1:
                    if time not in sensor_data:
                        sensor_data[time] = []
                    sensor_data[time].append([flow, speed, occupancy])
    # calculate mfd
    mfd_data = []
    for time in sensor_data:
        data = np.asarray(sensor_data[time])
        data = np.mean(data, axis=0)
        mfd_data.append([time, *data])
    mfd_data = pd.DataFrame(mfd_data, columns=["time", "flow", "speed", "occupancy"])
    # do 2nd order polynomial regression of mfd
    oc_fl = doPolynomialModel(mfd_data, "occupancy", "flow")
    oc_sp = doPolynomialModel(mfd_data, "occupancy", "speed")
    sp_fl = doPolynomialModel(mfd_data, "speed", "flow")
    return mfd_data, oc_fl, oc_sp, sp_fl




# PROCESS DATA
mfd_data_scen_1, oc_fl_scen_1, oc_sp_scen_1, sp_fl_scen_1 = loadMFD(path_to_results_scenario_1)
mfd_data_scen_2, oc_fl_scen_2, oc_sp_scen_2, sp_fl_scen_2 = loadMFD(path_to_results_scenario_2)
mfd_data_scen_3, oc_fl_scen_3, oc_sp_scen_3, sp_fl_scen_3 = loadMFD(path_to_results_scenario_3)




# VISUALIZATION
plt.figure(figsize=(10,3.5))
plt.suptitle("Macroscopic Fundamental Diagram")

plt.subplot(1,3,1)
plt.ylabel("Flow")
plt.xlabel("Occupancy")
plt.scatter(mfd_data_scen_1["occupancy"], mfd_data_scen_1["flow"], label="Scenario 1")
plt.plot(oc_fl_scen_1[0], oc_fl_scen_1[1], "--")
plt.scatter(mfd_data_scen_2["occupancy"], mfd_data_scen_2["flow"], label="Scenario 2")
plt.plot(oc_fl_scen_2[0], oc_fl_scen_2[1], "--")
plt.scatter(mfd_data_scen_3["occupancy"], mfd_data_scen_3["flow"], label="Scenario 3")
plt.plot(oc_fl_scen_3[0], oc_fl_scen_3[1], "--")
plt.ylim(0, max(max(mfd_data_scen_1["flow"]),max(mfd_data_scen_2["flow"]),max(mfd_data_scen_3["flow"]))*1.1)
plt.legend()

plt.subplot(1,3,2)
plt.ylabel("Speed")
plt.xlabel("Occupancy")
plt.scatter(mfd_data_scen_1["occupancy"], mfd_data_scen_1["speed"], label="Scenario 1")
plt.plot(oc_sp_scen_1[0], oc_sp_scen_1[1], "--")
plt.scatter(mfd_data_scen_2["occupancy"], mfd_data_scen_2["speed"], label="Scenario 2")
plt.plot(oc_sp_scen_2[0], oc_sp_scen_2[1], "--")
plt.scatter(mfd_data_scen_3["occupancy"], mfd_data_scen_3["speed"], label="Scenario 3")
plt.plot(oc_sp_scen_3[0], oc_sp_scen_3[1], "--")
plt.ylim(0, max(max(mfd_data_scen_1["speed"]), max(mfd_data_scen_2["speed"]), max(mfd_data_scen_3["speed"]))*1.1)
plt.legend()

plt.subplot(1,3,3)
plt.ylabel("Flow")
plt.xlabel("Speed")
plt.scatter(mfd_data_scen_1["speed"], mfd_data_scen_1["flow"], label="Scenario 1")
plt.plot(sp_fl_scen_1[0], sp_fl_scen_1[1], "--")
plt.scatter(mfd_data_scen_2["speed"], mfd_data_scen_2["flow"], label="Scenario 2")
plt.plot(sp_fl_scen_2[0], sp_fl_scen_2[1], "--")
plt.scatter(mfd_data_scen_3["speed"], mfd_data_scen_3["flow"], label="Scenario 3")
plt.plot(sp_fl_scen_3[0], sp_fl_scen_3[1], "--")
plt.ylim(0, max(max(mfd_data_scen_1["flow"]), max(mfd_data_scen_2["flow"]), max(mfd_data_scen_3["flow"]))*1.1)
plt.legend()

plt.tight_layout()