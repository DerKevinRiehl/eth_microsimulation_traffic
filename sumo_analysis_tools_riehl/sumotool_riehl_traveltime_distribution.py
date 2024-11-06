# IMPORTS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# PARAMTERS
path_scenario_1 = "../simulation_output/scenario_1_model/log_tripinfo.xml"
path_scenario_2 = "../simulation_output/scenario_2_model/log_tripinfo.xml"
path_scenario_3 = "../simulation_output/scenario_3_model/log_tripinfo.xml"



# METHODS
def loadTravelTimes(path):
    f = open(path, "r")
    content = f.read()
    f.close()
    lines = content.split("\n")
    lines = [line.strip() for line in lines]
    time_data = []
    for line in lines:
        if line.startswith("<tripinfo "):
            travel_time = float(line.split("duration=")[1].split("\"")[1])
            distance = float(line.split("routeLength=")[1].split("\"")[1])        
            wait_time = float(line.split("waitingTime=")[1].split("\"")[1])   
            loss_time = float(line.split("timeLoss=")[1].split("\"")[1])
            time_data.append([distance, travel_time, wait_time, loss_time])
    df_time = pd.DataFrame(time_data, columns=["distance", "travel_time", "wait_time", "loss_time"])
    df_time["av_speed"] = df_time["travel_time"] / df_time["distance"]
    return df_time

def drawDistributionOverDistance(df_time_1, df_time_2, df_time_3, measure):
    grouped_1 = df_time_1.groupby('distance').agg({measure: ['mean', 'std']}).reset_index()
    grouped_1.columns = ['distance', 'mean_travel_time', 'std_travel_time']
    grouped_1 = grouped_1.sort_values('distance')
    plt.gca().plot(grouped_1['distance'], grouped_1['mean_travel_time'], label='Scenario 1')
    plt.gca().fill_between(grouped_1['distance'], 
                    grouped_1['mean_travel_time'] - grouped_1['std_travel_time'],
                    grouped_1['mean_travel_time'] + grouped_1['std_travel_time'],
                    alpha=0.2)
    grouped_2 = df_time_2.groupby('distance').agg({measure: ['mean', 'std']}).reset_index()
    grouped_2.columns = ['distance', 'mean_travel_time', 'std_travel_time']
    grouped_2 = grouped_2.sort_values('distance')
    plt.gca().plot(grouped_2['distance'], grouped_2['mean_travel_time'], label='Scenario 2')
    plt.gca().fill_between(grouped_2['distance'], 
                    grouped_2['mean_travel_time'] - grouped_2['std_travel_time'],
                    grouped_2['mean_travel_time'] + grouped_2['std_travel_time'],
                    alpha=0.2)
    grouped_3 = df_time_3.groupby('distance').agg({measure: ['mean', 'std']}).reset_index()
    grouped_3.columns = ['distance', 'mean_travel_time', 'std_travel_time']
    grouped_3 = grouped_3.sort_values('distance')
    plt.gca().plot(grouped_3['distance'], grouped_3['mean_travel_time'], label='Scenario 3')
    plt.gca().fill_between(grouped_3['distance'], 
                    grouped_3['mean_travel_time'] - grouped_3['std_travel_time'],
                    grouped_3['mean_travel_time'] + grouped_3['std_travel_time'],
                    alpha=0.2)




# MAIN CODE 
df_time_1 = loadTravelTimes(path_scenario_1)
df_time_2 = loadTravelTimes(path_scenario_2)
df_time_3 = loadTravelTimes(path_scenario_3)

plt.figure(figsize=(15,8))

plt.subplot(2,4,1)
plt.title("Travel Time Distribution")
sns.kdeplot(data=df_time_1["travel_time"], shade=True, label="Scenario 1 [tot. "+str(int(sum(df_time_1["travel_time"])/60/60))+"h, av. "+"{:.2f}".format(np.mean(df_time_1["travel_time"]))+"s]")
sns.kdeplot(data=df_time_2["travel_time"], shade=True, label="Scenario 2 [tot. "+str(int(sum(df_time_2["travel_time"])/60/60))+"h, av. "+"{:.2f}".format(np.mean(df_time_2["travel_time"]))+"s]")
sns.kdeplot(data=df_time_3["travel_time"], shade=True, label="Scenario 3 [tot. "+str(int(sum(df_time_3["travel_time"])/60/60))+"h, av. "+"{:.2f}".format(np.mean(df_time_3["travel_time"]))+"s]")
plt.xlabel('Travel Time [s]')
plt.ylabel("")
plt.gca().set_yticklabels([])
plt.grid()
plt.legend(fontsize="small")
corner = plt.xlim()[1]/2
plt.gca().set_xlim(plt.xlim()[0], int(corner))

plt.subplot(2,4,2)
plt.title("Average Speed Distribution")
sns.kdeplot(data=df_time_1["av_speed"], shade=True, label="Scenario 1 [av. "+"{:.2f}".format(np.mean(df_time_1["av_speed"]))+"s]")
sns.kdeplot(data=df_time_2["av_speed"], shade=True, label="Scenario 2 [av. "+"{:.2f}".format(np.mean(df_time_2["av_speed"]))+"s]")
sns.kdeplot(data=df_time_3["av_speed"], shade=True, label="Scenario 3 [av. "+"{:.2f}".format(np.mean(df_time_3["av_speed"]))+"s]")
plt.xlabel('Speed [m/s]')
plt.ylabel("")
plt.gca().set_yticklabels([])
plt.grid()
plt.legend(fontsize="small")
corner = plt.xlim()[1]/2
plt.gca().set_xlim(plt.xlim()[0], int(corner))

plt.subplot(2,4,3)
plt.title("Waiting Time Distribution")
sns.kdeplot(data=df_time_1["wait_time"], shade=True, label="Scenario 1 [av. "+"{:.2f}".format(np.mean(df_time_1["wait_time"]))+"s]")
sns.kdeplot(data=df_time_2["wait_time"], shade=True, label="Scenario 2 [av. "+"{:.2f}".format(np.mean(df_time_2["wait_time"]))+"s]")
sns.kdeplot(data=df_time_3["wait_time"], shade=True, label="Scenario 3 [av. "+"{:.2f}".format(np.mean(df_time_3["wait_time"]))+"s]")
plt.xlabel('Wait Time [s]')
plt.ylabel("")
plt.gca().set_yticklabels([])
plt.grid()
plt.legend(fontsize="small")
corner = plt.xlim()[1]/2
plt.gca().set_xlim(plt.xlim()[0], int(corner))

plt.subplot(2,4,4)
plt.title("Delay Time Distribution")
sns.kdeplot(data=df_time_1["loss_time"], shade=True, label="Scenario 1 [av. "+"{:.2f}".format(np.mean(df_time_1["loss_time"]))+"s]")
sns.kdeplot(data=df_time_2["loss_time"], shade=True, label="Scenario 2 [av. "+"{:.2f}".format(np.mean(df_time_2["loss_time"]))+"s]")
sns.kdeplot(data=df_time_3["loss_time"], shade=True, label="Scenario 3 [av. "+"{:.2f}".format(np.mean(df_time_3["loss_time"]))+"s]")
plt.xlabel('Delay Time [s]')
plt.ylabel("")
plt.gca().set_yticklabels([])
plt.grid()
plt.legend(fontsize="small")
corner = plt.xlim()[1]/2
plt.gca().set_xlim(plt.xlim()[0], int(corner))

plt.subplot(2,4,5)
plt.title("Travel Time Distribution Over Distance")
plt.xlabel("Travel Distance [m]")
plt.ylabel("Travel Time [s]")
drawDistributionOverDistance(df_time_1, df_time_2, df_time_3, measure="travel_time")
plt.legend()

plt.subplot(2,4,6)
plt.title("Average Speed Distribution Over Distance")
plt.xlabel("Travel Distance [m]")
plt.ylabel("Average Speed [m/s]")
drawDistributionOverDistance(df_time_1, df_time_2, df_time_3, measure="av_speed")
plt.legend()

plt.subplot(2,4,7)
plt.title("Waiting Time Distribution Over Distance")
plt.xlabel("Travel Distance [m]")
plt.ylabel("Wait Time [s]")
drawDistributionOverDistance(df_time_1, df_time_2, df_time_3, measure="wait_time")
plt.legend()

plt.subplot(2,4,8)
plt.title("Delay Time Distribution Over Distance")
plt.xlabel("Travel Distance [m]")
plt.ylabel("Loss Time [s]")
drawDistributionOverDistance(df_time_1, df_time_2, df_time_3, measure="loss_time")
plt.legend()

plt.tight_layout()