# main.py
import json
import numpy as np
import networkx as nx
from python_tsp.exact import solve_tsp_dynamic_programming
from interface import get_optimization_criteria  # Import the function from interface.py
from graph_utils import build_graph, plot_graph  # Import functions from graph_utils.py
import time
from logger_config import logger  # Import the logger

def parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    logger.info(f"Parsed JSON data from {filename}.")
    return data

def compute_all_pairs_shortest_paths(G):
    # Use Floyd-Warshall algorithm to compute shortest paths
    all_pairs = dict(nx.floyd_warshall(G, weight='weight'))
    logger.info("Computed all-pairs shortest paths.")
    return all_pairs

def main():
    # Start timing
    start_time = time.perf_counter()

    # Get the optimization criteria from the user
    criteria = get_optimization_criteria()
    logger.info(f"Selected optimization criteria: {criteria}")

    # Parse the JSON data
    data = parse_json('data/routes.json')

    # Build the graph
    G = build_graph(data, criteria)

    # Compute all-pairs shortest paths based on chosen criteria
    all_pairs = compute_all_pairs_shortest_paths(G)

    # Build the distance matrix for TSP solver
    nodes = list(G.nodes())
    n = len(nodes)
    index = {nodes[i]: i for i in range(n)}
    distance_matrix = np.zeros((n, n))
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            distance_matrix[i][j] = all_pairs[u][v]
    logger.info("Constructed distance matrix for TSP solver.")

    # Solve TSP using python-tsp
    tsp_start_time = time.perf_counter()
    permutation, total_weight = solve_tsp_dynamic_programming(distance_matrix)
    tsp_end_time = time.perf_counter()
    tsp_duration = tsp_end_time - tsp_start_time
    logger.info(f"TSP solver executed in {tsp_duration:.4f} seconds.")

    # Adjust permutation to start at 'Tarjan's Home'
    start_index = index["Tarjan's Home"]
    start_pos = list(permutation).index(start_index)
    permutation = np.roll(permutation, -start_pos)
    # Get the optimal path
    optimal_path = [nodes[i] for i in permutation]
    logger.info(f"Optimal path determined: {optimal_path}")

    if criteria == 'time':
        logger.info(f"Total travel time: {total_weight:.2f} hours")
    elif criteria == 'cost':
        logger.info(f"Total travel cost: {total_weight:.2f} units")
    elif criteria == 'transfers':
        logger.info(f"Total number of transfers: {total_weight:.0f}")
    else:
        logger.info(f"Total weight: {total_weight:.2f}")

    # End timing
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.info(f"Program execution time: {elapsed_time:.4f} seconds")

    # Output to console
    print("Optimal path to visit all relatives:")
    for node in optimal_path:
        print(node)
    if criteria == 'time':
        print(f"Total travel time: {total_weight:.2f} hours")
    elif criteria == 'cost':
        print(f"Total travel cost: {total_weight:.2f} units")
    elif criteria == 'transfers':
        print(f"Total number of transfers: {total_weight:.0f}")
    else:
        print(f"Total weight: {total_weight:.2f}")

    # Plot the graph with the optimal path and criteria
    plot_graph(G, optimal_path, criteria)

if __name__ == "__main__":
    main()
