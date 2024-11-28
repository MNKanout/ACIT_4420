import json
from geopy.distance import geodesic


def load_json(file_path):
    """
    Load JSON data from a file.
    pi
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        dict: Parsed JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in the file '{file_path}'.")
        return {}


def calculate_distance(coord1, coord2):
    """
    Calculate the geographical distance between two coordinates.
    
    Args:
        coord1 (tuple): Tuple of (latitude, longitude) for the first location.
        coord2 (tuple): Tuple of (latitude, longitude) for the second location.
    
    Returns:
        float: Distance in kilometers.
    """
    return geodesic(coord1, coord2).kilometers