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
    # Validate the coordinates before calculating
    validate_coordinates(coord1)
    validate_coordinates(coord2)
    return geodesic(coord1, coord2).kilometers



def validate_coordinates(coord):
    """
    Validate that a coordinate tuple contains valid latitude and longitude.

    Args:
        coord (tuple): Tuple of (latitude, longitude).

    Raises:
        ValueError: If the latitude or longitude is out of range.
    """
    lat, lon = coord
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")