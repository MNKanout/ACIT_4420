# main.py
import time
from modules.data_loader import parse_json
from modules.graph_utils import (
    build_graph,
    compute_all_pairs_shortest_paths,
    create_distance_matrix,
    plot_graph
)
from modules.optimizer import solve_tsp, adjust_route
from modules.presenter import log_total_weight, output_results
from modules.interface import get_optimization_criteria  # Import the function from interface.py
from modules.logger_config import logger  # Import the logger


def main():
    """
    Main function to execute the TarjanPlanner program.
    """
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
    distance_matrix, index, nodes = create_distance_matrix(G, all_pairs)

    # Solve TSP using python-tsp
    permutation, total_weight = solve_tsp(distance_matrix)

    # Adjust permutation to start at 'Tarjan's Home'
    optimal_path = adjust_route(permutation, index, nodes)

    # Log total weight based on criteria
    log_total_weight(criteria, total_weight)

    # End timing
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Program execution time: {elapsed_time:.4f} seconds")

    # Output results to console
    output_results(optimal_path, criteria, total_weight)

    # Plot the graph with the optimal path and criteria
    plot_graph(G, optimal_path, criteria)


if __name__ == "__main__":
    main()
