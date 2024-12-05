# presenter.py
from .logger_config import logger


def log_total_weight(criteria, total_weight):
    """
    Logs the total weight based on the selected optimization criteria.
    
    Parameters:
        criteria (str): The selected optimization criteria ('time', 'cost', 'transfers').
        total_weight (float): The total weight calculated by the optimizer.
    """
    if criteria == 'time':
        logger.info(f"Total travel time: {total_weight:.2f} hours")
    elif criteria == 'cost':
        logger.info(f"Total travel cost: {total_weight:.2f} units")
    elif criteria == 'transfers':
        logger.info(f"Total number of transfers: {total_weight:.0f}")
    else:
        logger.info(f"Total weight: {total_weight:.2f}")


def output_results(optimal_path, criteria, total_weight):
    """
    Outputs the optimized route and associated metrics to the console.
    
    Parameters:
        optimal_path (list): The sequence of locations to visit.
        criteria (str): The selected optimization criteria.
        total_weight (float): The total weight corresponding to the criteria.
    """
    print("\nOptimal path to visit all relatives:")
    for node in optimal_path:
        print(node)
    print()
    if criteria == 'time':
        print(f"Total travel time: {total_weight:.2f} hours")
    elif criteria == 'cost':
        print(f"Total travel cost: {total_weight:.2f} units")
    elif criteria == 'transfers':
        print(f"Total number of transfers: {total_weight:.0f}")
    else:
        print(f"Total weight: {total_weight:.2f}")
