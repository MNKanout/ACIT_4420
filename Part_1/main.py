import json
import numpy as np
import networkx as nx
from geopy.distance import geodesic
from python_tsp.exact import solve_tsp_dynamic_programming
from interface import get_optimization_criteria  # Import the function from interface.py

def parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def build_graph(data, criteria):
    G = nx.Graph()
    for route in data:
        pos1 = route['position_1']
        pos2 = route['position_2']
        coord1 = tuple(route['position1_coordinates'])
        coord2 = tuple(route['position2_coordinates'])
        travel_speed = route['travel_speed']
        cost_per_km = route['cost_per_km']
        travel_mode = route['travel_mode']

        # Calculate distance using geopy
        distance = geodesic(coord1, coord2).kilometers
        # Calculate time and cost
        time = distance / travel_speed
        cost = distance * cost_per_km

        # Determine the edge weight based on criteria
        if criteria == 'time':
            weight = time
        elif criteria == 'cost':
            weight = cost
        elif criteria == 'transfers':
            # For transfers, assign a weight of 1 per edge
            weight = 1
        else:
            weight = time  # default to time

        # Add nodes and edge
        G.add_node(pos1, coordinates=coord1)
        G.add_node(pos2, coordinates=coord2)
        G.add_edge(pos1, pos2, weight=weight, distance=distance, time=time, cost=cost, travel_mode=travel_mode)
    return G

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

if __name__ == "__main__":
    main()
