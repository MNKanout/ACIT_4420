# graph_utils.py
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from logger_config import logger  # Import the logger

def build_graph(data, criteria):
    G = nx.Graph()
    logger.info("Building the graph.")
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

        # Add nodes and edge to the graph
        G.add_node(pos1, coordinates=coord1)
        G.add_node(pos2, coordinates=coord2)
        G.add_edge(pos1, pos2, weight=weight, distance=distance, time=time,
                   cost=cost, travel_mode=travel_mode)
        logger.debug(f"Added edge from {pos1} to {pos2} with weight {weight:.4f}")

    logger.info("Graph construction completed.")
    return G

def plot_graph(G, optimal_path, criteria):
    # Prepare positions for plotting
    nodes_positions = {}
    for node in G.nodes():
        coord = G.nodes[node]['coordinates']
        # Note: Positions need to be in (longitude, latitude) for plotting
        nodes_positions[node] = (coord[1], coord[0])

    plt.figure(figsize=(12, 8))

    # Draw all edges
    nx.draw_networkx_edges(G, pos=nodes_positions, edge_color='gray', alpha=0.5)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos=nodes_positions, node_size=300, node_color='blue')

    # Draw labels
    nx.draw_networkx_labels(G, pos=nodes_positions, font_size=9, font_color='black')

    # Highlight the optimal path
    path_edges = list(zip(optimal_path, optimal_path[1:] + [optimal_path[0]]))
    nx.draw_networkx_edges(G, pos=nodes_positions, edgelist=path_edges, edge_color='red', width=2)

    # Set the title based on the criteria
    if criteria == 'time':
        title = 'Tarjan\'s Optimal Path (Shortest Travel Time)'
    elif criteria == 'cost':
        title = 'Tarjan\'s Optimal Path (Least Cost)'
    elif criteria == 'transfers':
        title = 'Tarjan\'s Optimal Path (Minimal Number of Transfers)'
    else:
        title = 'Tarjan\'s Optimal Path to Visit All Relatives'

    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.axis('equal')
    logger.info("Displaying the plot.")
    plt.show()
