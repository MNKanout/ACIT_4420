import sys
import pytest
from pathlib import Path

# Add Part_1 to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import the function to test
from utils import load_json

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

# Main function to execute the tests
if __name__ == "__main__":
    # Run all tests
    print("Running tests...")
    
    # Using pytest's main to run tests programmatically
    pytest.main(["-v", __file__])
