import json
import math
import itertools
import networkx as nx


def haversine(coord1, coord2):
    # Calculate the great-circle distance between two coordinates
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def build_graph(data):
    G = nx.Graph()
    for route in data:
        pos1 = route['position_1']
        pos2 = route['position_2']
        coord1 = tuple(route['position1_coordinates'])
        coord2 = tuple(route['position2_coordinates'])
        travel_speed = route['travel_speed']
        cost_per_km = route['cost_per_km']
        travel_mode = route['travel_mode']

        # Calculate distance
        distance = haversine(coord1, coord2)
        # Calculate time and cost
        time = distance / travel_speed
        cost = distance * cost_per_km

        # Add nodes and edge
        G.add_node(pos1, coordinates=coord1)
        G.add_node(pos2, coordinates=coord2)
        G.add_edge(pos1, pos2, distance=distance, time=time, cost=cost, travel_mode=travel_mode)
    return G

def compute_all_pairs_shortest_paths(G, weight):
    # Use Floyd-Warshall algorithm to compute shortest paths
    return dict(nx.floyd_warshall(G, weight=weight))

def held_karp(dists):
    """
    Implementation of the Held-Karp algorithm to solve the TSP.
    dists: 2D dictionary of distances between nodes.
    Returns the optimal path and its cost.
    """
    n = len(dists)
    nodes = list(dists.keys())
    # Maps each subset of the nodes to the cost to reach that subset, ending at a particular node.
    C = {}
    # Initialize with the direct distances from the start node (Tarjan's Home)
    start = nodes.index("Tarjan's Home")
    index = {nodes[i]: i for i in range(n)}
    for k in range(n):
        if k == start:
            continue
        C[(1 << start) | (1 << k), k] = (dists["Tarjan's Home"][nodes[k]], [start, k])

    for subset_size in range(3, n + 1):
        for subset in [bits for bits in itertools.combinations(range(n), subset_size) if start in bits]:
            bits_set = sum([1 << b for b in subset])
            for k in subset:
                if k == start:
                    continue
                prev_bits = bits_set & ~(1 << k)
                res = []
                for m in subset:
                    if m == start or m == k:
                        continue
                    if (prev_bits, m) in C:
                        cost, path = C[(prev_bits, m)]
                        res.append((cost + dists[nodes[m]][nodes[k]], path + [k]))
                if res:
                    C[(bits_set, k)] = min(res)
    # Final step
    bits_set = (1 << n) - 1
    res = []
    for k in range(n):
        if k == start:
            continue
        if (bits_set, k) in C:
            cost, path = C[(bits_set, k)]
            res.append((cost, path))
    min_cost, min_path = min(res)
    optimal_path = [nodes[i] for i in min_path]
    return min_cost, optimal_path

def main():
    # Parse the JSON data
    data = parse_json('routes.json')
    # Build the graph
    G = build_graph(data)
    # Compute all-pairs shortest paths based on travel time
    all_pairs = compute_all_pairs_shortest_paths(G, weight='time')
    # Build the distance matrix for Held-Karp algorithm
    nodes = list(G.nodes())
    dists = {}
    for u in nodes:
        dists[u] = {}
        for v in nodes:
            if u == v:
                dists[u][v] = 0
            else:
                dists[u][v] = all_pairs[u][v]
    # Solve TSP using Held-Karp algorithm
    min_cost, optimal_path = held_karp(dists)
    print("Optimal path to visit all relatives:")
    for node in optimal_path:
        print(node)
    print(f"Total travel time: {min_cost:.2f} hours")

if __name__ == "__main__":
    main()
