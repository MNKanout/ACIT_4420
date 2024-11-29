import json
import numpy as np
import networkx as nx
from python_tsp.exact import solve_tsp_dynamic_programming
from interface import get_optimization_criteria  # Import the function from interface.py
from graph_utils import build_graph, plot_graph  # Import functions from graph_utils.py

def parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def compute_all_pairs_shortest_paths(G):
    # Use Floyd-Warshall algorithm to compute shortest paths
    return dict(nx.floyd_warshall(G, weight='weight'))

def main():
    # Get the optimization criteria from the user
    criteria = get_optimization_criteria()
    # Parse the JSON data
    data = parse_json('routes.json')
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
    # Solve TSP using python-tsp
    permutation, total_weight = solve_tsp_dynamic_programming(distance_matrix)
    # Adjust permutation to start at 'Tarjan's Home'
    start_index = index["Tarjan's Home"]
    start_pos = list(permutation).index(start_index)
    permutation = np.roll(permutation, -start_pos)
    # Get the optimal path
    optimal_path = [nodes[i] for i in permutation]
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
