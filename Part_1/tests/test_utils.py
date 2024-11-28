import sys
import pytest
from pathlib import Path

# Add Part_1 to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import the function to test
from utils import load_json, calculate_distance, validate_coordinates

# Test functions
def test_load_json_valid_file(tmp_path):
    """
    Test loading a valid JSON file.
    """
    # Create a temporary valid JSON file
    test_data = {"key": "value"}
    json_file = tmp_path / "valid.json"
    json_file.write_text('{"key": "value"}')
    
    # Load the file using the function
    result = load_json(json_file)
    
    # Assert the content is as expected
    assert result == test_data


def test_load_json_missing_file():
    """
    Test loading a missing JSON file.
    """
    # Try to load a non-existent file
    result = load_json("non_existent_file.json")
    
    # Assert the function returns an empty dictionary
    assert result == {}


def test_load_json_invalid_json(tmp_path):
    """
    Test loading an invalid JSON file.
    """
    # Create a temporary invalid JSON file
    json_file = tmp_path / "invalid.json"
    json_file.write_text("{invalid: json}")  # Invalid JSON content
    
    # Try to load the invalid file
    result = load_json(json_file)
    
    # Assert the function returns an empty dictionary
    assert result == {}


def test_calculate_distance_valid_coordinates():
    """
    Test calculate_distance with valid coordinates.
    """
    # Coordinates for Seoul and Incheon
    coord1 = (37.5665, 126.9780)  # Seoul
    coord2 = (37.4563, 126.7052)  # Incheon
    
    # Calculate the distance
    distance = calculate_distance(coord1, coord2)
    
    # Assert the result is within an expected range (around 27 km)
    assert 25 <= distance <= 30


def test_calculate_distance_same_coordinates():
    """
    Test calculate_distance when both coordinates are the same.
    """
    coord = (37.5665, 126.9780)  # Seoul
    
    # Calculate the distance
    distance = calculate_distance(coord, coord)
    
    # Assert the distance is zero
    assert distance == 0


def test_calculate_distance_extreme_coordinates():
    """
    Test calculate_distance with extreme valid coordinates.
    """
    # North Pole and South Pole
    coord1 = (90.0, 0.0)    # North Pole
    coord2 = (-90.0, 0.0)   # South Pole
    
    # Calculate the distance
    distance = calculate_distance(coord1, coord2)
    
    # Assert the result is around 20,000 km (Earth's approximate diameter)
    assert 20000 <= distance <= 20100


def test_calculate_distance_invalid_coordinates():
    """
    Test calculate_distance with invalid coordinates.
    """
    # Invalid coordinates
    coord1 = (91.0, 0.0)    # Latitude out of range
    coord2 = (37.5665, 126.9780)
    
    # Expect a ValueError from geopy
    with pytest.raises(ValueError):
        calculate_distance(coord1, coord2)


def test_validate_coordinates_valid():
    """
    Test validate_coordinates with valid latitude and longitude.
    """
    valid_coords = [
        (0, 0),           # Equator and Prime Meridian
        (45, 90),         # North-East Quadrant
        (-45, -90),       # South-West Quadrant
        (90, 180),        # Maximum valid values
        (-90, -180),      # Minimum valid values
    ]
    for coord in valid_coords:
        # Should not raise an exception
        validate_coordinates(coord)


def test_validate_coordinates_invalid_latitude():
    """
    Test validate_coordinates with invalid latitude values.
    """
    invalid_latitudes = [
        (91, 0),    # Latitude > 90
        (-91, 0),   # Latitude < -90
    ]
    for coord in invalid_latitudes:
        with pytest.raises(ValueError, match="Invalid latitude"):
            validate_coordinates(coord)


def test_validate_coordinates_invalid_longitude():
    """
    Test validate_coordinates with invalid longitude values.
    """
    invalid_longitudes = [
        (0, 181),   # Longitude > 180
        (0, -181),  # Longitude < -180
    ]
    for coord in invalid_longitudes:
        with pytest.raises(ValueError, match="Invalid longitude"):
            validate_coordinates(coord)


def test_validate_coordinates_invalid_both():
    """
    Test validate_coordinates with both latitude and longitude invalid.
    """
    invalid_coords = [
        (91, 181),   # Both latitude and longitude out of range
        (-91, -181), # Both latitude and longitude out of range
    ]
    for coord in invalid_coords:
        with pytest.raises(ValueError):
            validate_coordinates(coord)