# #############################################################################
# IMPORTS
# #############################################################################
import numpy as np
from scipy.optimize import minimize_scalar
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from scipy.optimize import minimize




# #############################################################################
# CLASS
# #############################################################################
class Algorithm_EntropyMaximization:
    def __init__(self, entrances, exits, mask_matrix):
        self.entrances = np.array(entrances)
        self.exits = np.array(exits)
        self.mask_matrix = np.array(mask_matrix)
        self.n_origins = len(entrances)
        self.n_destinations = len(exits)
        self.total_flow = sum(entrances)
        
    def estimate_OD(self, initial_guess, max_iter=100, tolerance=1e-6):
        od_matrix = initial_guess
        for _ in range(max_iter):
            old_od_matrix = od_matrix.copy()
            # Row balancing
            row_factors = self.entrances / np.sum(od_matrix, axis=1)
            od_matrix = od_matrix * row_factors[:, np.newaxis]
            # Column balancing
            col_factors = self.exits / np.sum(od_matrix, axis=0)
            od_matrix = od_matrix * col_factors
            # Check convergence
            if np.max(np.abs(od_matrix - old_od_matrix)) < tolerance:
                break
        return od_matrix

class Algorithm_GravityModel:
    def __init__(self, entrances, exits, mask_matrix, cost_matrix):
        self.entrances = np.array(entrances)
        self.exits = np.array(exits)
        self.mask_matrix = np.array(mask_matrix)
        self.n_origins = len(entrances)
        self.n_destinations = len(exits)
        self.total_flow = sum(entrances)
        self.cost_matrix = cost_matrix
        
    def estimate_OD(self, initial_guess, beta=1):
       # Initialize parameters
       A = np.ones(self.n_origins)
       B = np.ones(self.n_destinations)
       def objective(params):
           A = params[:self.n_origins]
           B = params[self.n_origins:]
           T = np.outer(A * self.entrances, B * self.exits) / (self.cost_matrix ** beta)
           T *= self.mask_matrix  # Apply mask
           row_sum_diff = np.sum(T, axis=1) - self.entrances
           col_sum_diff = np.sum(T, axis=0) - self.exits
           return np.sum(row_sum_diff**2) + np.sum(col_sum_diff**2)
       # Optimize
       result = minimize(objective, np.concatenate([A, B]), method='L-BFGS-B')
       optimal_params = result.x
       # Reconstruct OD matrix
       A_opt = optimal_params[:self.n_origins]
       B_opt = optimal_params[self.n_origins:]
       od_matrix = np.outer(A_opt * self.entrances, B_opt * self.exits) / (self.cost_matrix ** beta)
       od_matrix *= self.mask_matrix  # Apply mask
       return od_matrix

class Algorithm_Frank_Wolfe:
    def __init__(self, entrances, exits, mask_matrix):
        self.entrances = np.array(entrances)
        self.exits = np.array(exits)
        self.mask_matrix = np.array(mask_matrix)
        self.n_origins = len(entrances)
        self.n_destinations = len(exits)
        self.total_flow = sum(entrances)
    
    def _gradient(self, od_matrix):
        grad = np.zeros_like(od_matrix)
        row_diff = np.sum(od_matrix, axis=1) - self.entrances
        col_diff = np.sum(od_matrix, axis=0) - self.exits
        for i in range(self.n_origins):
            for j in range(self.n_destinations):
                if self.mask_matrix[i, j] != 0:
                    grad[i,j] = 2 * (row_diff[i] + col_diff[j])
        return grad

    def _step(self, od_matrix, gradient):
        s = np.zeros_like(od_matrix)
        masked_gradient = np.where(self.mask_matrix != 0, gradient, np.inf)
        s[np.unravel_index(np.argmin(masked_gradient), gradient.shape)] = self.total_flow
        return s
    
    def _objective_function(self, od_matrix):
        row_sum_diff = np.sum((np.sum(od_matrix, axis=1) - self.entrances)**2)
        col_sum_diff = np.sum((np.sum(od_matrix, axis=0) - self.exits)**2)
        return row_sum_diff + col_sum_diff
    
    def estimate_OD(self, initial_guess, max_iter=100, tolerance=1e-6):
        od_matrix = initial_guess
        for iteration in range(max_iter):
            grad = self._gradient(od_matrix)
            s = self._step(od_matrix, grad)
            def obj(alpha):
                new_od = (1 - alpha) * od_matrix + alpha * s
                new_od *= self.mask_matrix
                return self._objective_function(new_od)
            res = minimize_scalar(obj, bounds=(0, 1), method='bounded')
            new_od = (1 - res.x) * od_matrix + res.x * s
            new_od *= self.mask_matrix
            if np.linalg.norm(new_od - od_matrix) < tolerance:
                break
            od_matrix = new_od
        return od_matrix
        
class OD_MatrixEstimator:
    def __init__(self, entrances, exits, mask_matrix, algorithm="Frank-Wolfe", cost_matrix=None):
        self.entrances = np.array(entrances)
        self.exits = np.array(exits)
        self.mask_matrix = np.array(mask_matrix)
        self.n_origins = len(entrances)
        self.n_destinations = len(exits)
        self.total_flow = sum(entrances)
        if algorithm=="Frank-Wolfe":
            self.algorithm = Algorithm_Frank_Wolfe(entrances, exits, mask_matrix)
        elif algorithm=="Entropy-Maximization":
            self.algorithm = Algorithm_EntropyMaximization(entrances, exits, mask_matrix)
        elif algorithm=="Gravity-Model":
            self.algorithm = Algorithm_GravityModel(entrances, exits, mask_matrix, cost_matrix)
            
    def random_initial_guess(self):
        # Random initial guess
        od_matrix = np.random.rand(self.n_origins, self.n_destinations)
        od_matrix *= self.mask_matrix
        # Normalize to match total flow
        od_matrix *= self.total_flow / np.sum(od_matrix)
        return od_matrix
    
    def run_estimation(self):
        initial_guess = self.random_initial_guess()
        result = self.algorithm.estimate_OD(initial_guess)
        return result

def normalize_OD_Matrix(estimated_od_matrix):
    row_sums = estimated_od_matrix.sum(axis=1, keepdims=True)
    estimated_od_matrix2 = estimated_od_matrix / row_sums
    estimated_od_matrix2 = np.nan_to_num(estimated_od_matrix2, nan=0.0)
    return estimated_od_matrix2




# #############################################################################
# EXAMPLE USAGE
# #############################################################################

# estimator = OD_MatrixEstimator(entrances, exits, mask_matrix, algorithm="Frank-Wolfe")
# best_matrix = estimator.run_estimation()
# best_matrix = normalize_OD_Matrix(best_matrix)

# estimator2 = OD_MatrixEstimator(entrances, exits, mask_matrix, algorithm="Entropy-Maximization")
# best_matrix2 optimal_k2 = estimator.run_estimation()
# best_matrix2 = normalize_OD_Matrix(best_matrix2)

