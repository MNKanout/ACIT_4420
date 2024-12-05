# data_loader.py
import json
from .logger_config import logger

def parse_json(filename):
    """
    Parses the JSON file and returns the data.
    
    Parameters:
        filename (str): The path to the JSON file.
        
    Returns:
        dict: Parsed JSON data.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        logger.info(f"Parsed JSON data from {filename}.")
        return data
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file {filename}.")
        raise
