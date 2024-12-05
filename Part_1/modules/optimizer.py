# optimizer.py
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from .logger_config import logger


def solve_tsp(distance_matrix):
    """
    Solves the Traveling Salesman Problem using dynamic programming.
    
    Parameters:
        distance_matrix (numpy.ndarray): The distance matrix for TSP.
        
    Returns:
        tuple: Optimal permutation of nodes, total weight.
    """
    permutation, total_weight = solve_tsp_dynamic_programming(distance_matrix)
    logger.info("Solved Traveling Salesman Problem.")
    return permutation, total_weight


def adjust_route(permutation, index, nodes):
    """
    Adjusts the permutation to start at the designated starting point.
    
    Parameters:
        permutation (list): The permutation of node indices.
        index (dict): Mapping of node names to their indices.
        nodes (list): List of node names.
        
    Returns:
        list: Optimized path starting from the designated point.
    """
    try:
        start_index = index["Tarjan's Home"]
        start_pos = list(permutation).index(start_index)
        permutation = np.roll(permutation, -start_pos)
        optimal_path = [nodes[i] for i in permutation]
        logger.info(f"Optimal path determined: {optimal_path}")
        return optimal_path
    except KeyError:
        logger.error("'Tarjan's Home' not found in the nodes.")
        raise
    except ValueError:
        logger.error("'Tarjan's Home' is not in the permutation.")
        raise
