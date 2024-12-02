# #############################################################################
# Imports
# #############################################################################
import numpy as np
from scipy.optimize import minimize_scalar
import pandas as pd
from sumotool_riehl_OD_Matrix_Estimation_tools import OD_MatrixEstimator, normalize_OD_Matrix
import warnings
warnings.filterwarnings("ignore")




# #############################################################################
# Paths & Parameters
# #############################################################################

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

# Defining possible Routes
possible_routes_list = {
	"E1":  ["A1", "A2","A3","A4","A5","A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E2":  ["A3","A4","A5","A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E3":  ["A4","A5","A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E4":  ["A5","A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E4b":	["A5","A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E5":  ["A6","A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E6":  ["A7","A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E7":  ["A8","A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E8":  ["A9","A10","A11f","A11","A12","A13","A14","A15"],
	"E9":  ["A10","A11f","A11","A12","A13","A14","A15"],
	"E10": ["A11f","A11","A12","A13","A14","A15"],
	"E11": ["A12","A13","A14","A15"],
	"E12": ["A13","A14","A15"],
	"E13": ["A14","A15"],
	"E14": ["A15"],
	"E15": ["AEnd"],
}


# #############################################################################
# Main Code
# #############################################################################

# ## DETERMINE MASK MATRIX
mask_matrix = np.zeros((len(input_list), len(output_list)))
for entrance in possible_routes_list:
    for exitance in possible_routes_list[entrance]:
        idx1 = list(input_list.keys()).index(entrance)
        idx2 = list(output_list.keys()).index(exitance)
        mask_matrix[idx1][idx2] = 1

folder_target_od = "od_matrix/"

# ## DETERMINE INPUT OUTPUT VECTOR
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

output_vector = [
    6388.14,
    6388.14,
    7783.86,
    32186.25,
    1495.84,
    6694.22,
    13366.08,
    15233.83,
    6528.78,
    5335.22,
    25557.12,
    16794.68,
    6422.37,
    6422.37,
    6422.37,
    6422.37,
    55844.74
]

# ## DETERMINE OD-MATRIX

# FRANK-WOLFE
try:
    estimator = OD_MatrixEstimator(input_vector, output_vector, mask_matrix, algorithm="Frank-Wolfe")
    best_matrix = estimator.run_estimation()
    best_matrix = normalize_OD_Matrix(best_matrix)
    np.savetxt(folder_target_od+"run_frank_wolfe"+".csv", best_matrix, delimiter=',', fmt='%.10f')
    print("\tsuccess FRANK-WOLFE")
except:
    print("\tfailed FRANK-WOLFE")
    
# ENTROPY_MAXIMIZATION
try:
    estimator2 = OD_MatrixEstimator(input_vector, output_vector, mask_matrix, algorithm="Entropy-Maximization")
    best_matrix2 = estimator.run_estimation()
    best_matrix2 = normalize_OD_Matrix(best_matrix2)
    np.savetxt(folder_target_od+"run_entropy_maxim"+".csv", best_matrix2, delimiter=',', fmt='%.10f')
    print("\tsuccess ENTROPY_MAXIMIZATION")
except:
    print("\tfailed ENTROPY_MAXIMIZATION")

"""
# GRAVITY_MODEL
try:
    estimator3 = OD_MatrixEstimator(input_vector, output_vector, mask_matrix, algorithm="Gravity-Model", cost_matrix=cost_matrix)
    best_matrix3 = estimator.run_estimation()
    best_matrix3 = normalize_OD_Matrix(best_matrix3)
    np.savetxt(folder_target_od+"run_gravity_model"+".csv", best_matrix3, delimiter=',', fmt='%.10f')
    print("\tsuccess GRAVITY_MODEL")
except:
    print("\tfailed GRAVITY_MODEL")
"""