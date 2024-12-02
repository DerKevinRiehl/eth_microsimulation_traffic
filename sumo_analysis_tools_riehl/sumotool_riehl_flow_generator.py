# #############################################################################
# Imports
# #############################################################################
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")




# #############################################################################
# Paths & Parameters
# #############################################################################

folder_od = "od_matrix/"
od_type              = "run_frank_wolfe"


input_list = {
	"E1":  "29380609",
	"E2":  "237823368",
	"E3":  "294719471#2",
	"E4":  "113980043",
	"E4b":  "33212769",
	"E5":  "114320572",
	"E6":  "35164818#1",
	"E7":  "112581690#1",
	"E8":  "917413773",
	"E9":  "114608771",
	"E10": "32024073",
	"E11": "28100819",
	"E12": "54856675",
	"E13": "55121417",
	"E14": "55364917#1",
	"E15": "24729570#1",
}

lanes_per_entrance = {
	"E1":  3,
	"E2":  1,
	"E3":  1,
	"E4":  1,
	"E4b": 1,
	"E5":  1,
	"E6":  1,
	"E7":  1,
	"E8":  1,
	"E9":  1,
	"E10": 1,
	"E11": 1,
	"E12": 1,
	"E13": 1,
	"E14": 1,
	"E15": 1,
}

output_list = {
	"A1":  "34211800",
	"A2":  "100553197",
	"A3":  "237821831",
	"A4":  "107041762",
	"A5":  "33212385",
	"A6":  "35164820",
	"A7":  "33214016#0",
	"A8":  "84504729",
	"A9":  "975794529",
	"A10": "32024114",
	"A11f": "28100151#0-AddedOffRampEdge",
	"A11": "28100837",
	"A12": "28100818",
	"A13": "e13",
	"A14": "55364925",
	"A15": "24729450",
	"AEnd": "24730010#1-AddedOnRampEdge"  #shall I include this as end edge?
}

input_vector = [
    51105.12,
    13957.18,
    10410.91,
    7477.00,
    11215.50,
    5056.92,
    10983.72,
    9885.35,
    11862.41,
    13922.35,
    12147.24,
    9500.00,
    9000.00,
    9000.00,
    8000.00,
    7500.00
]

# #############################################################################
# Main Code
# #############################################################################


# ## LOAD DATA
odmatrix = np.loadtxt(folder_od+od_type+".csv", delimiter=",")

# Create Flows for SUMO XML
delta = 0.01

table = []
for entrance in input_list:
    idx_entr = list(input_list.keys()).index(route_from)
    # determine flow for entrance and time
    flow = input_vector[idx_entr]
    # decide to spawn car or not
    probability_total_flow = flow/3600
    
    for exitLane in output_list:
        idx_exit = list(output_list.keys()).index(route_to)
        
        route_from = entrance
        route_to = exitLane
        
        probability = probability_total_flow*odmatrix[idx_entr][idx_exit]
    
        time_from = 0
        time_to = 3600
        
        string = ""
        string = "<flow id=\"flow_"+str(time_slot)+"_"+veh_type+"_route_"+route_from+"_"+route_to+"\" "
        string += "type=\""+veh_type+"\" "
        string += "probability=\""+str(probability)+"\" "
        string += "route=\"route_"+route_from+"_"+route_to+"\" "
        string += "begin=\""+str(time_from)+"\" "
        string += "end=\""+str(time_to)+"\" "
        string += "> </flow>"
        
        if probability>0:
            print(string)
