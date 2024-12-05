# TarjanPlanner

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Running Unit Tests](#running-unit-tests)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

**TarjanPlanner** is a route optimization tool designed to determine the most efficient path for visiting all specified locations based on user-defined criteria such as travel time, cost, or the number of transfers. Leveraging advanced algorithms and a structured data approach, TarjanPlanner assists users in planning optimal travel routes within a transportation network.

## Features

- **Flexible Optimization Criteria**: Choose to optimize for shortest travel time, least cost, or minimal number of transfers.
- **Comprehensive Route Data Handling**: Parses and processes detailed route information from a JSON data source.
- **Graph-Based Analysis**: Constructs and analyzes a transport network graph to compute optimal paths.
- **Visualization**: Generates visual representations of the transport network and highlights the optimal route.
- **Robust Logging**: Maintains detailed logs of operations, aiding in monitoring and debugging.
- **Unit Testing**: Ensures reliability and correctness through comprehensive unit tests for each module.

## Directory Structure

. ├── data │ └── routes.json ├── main.py ├── modules │ ├── init.py │ ├── data_loader.py │ ├── graph_utils.py │ ├── interface.py │ ├── logger_config.py │ ├── optimizer.py │ └── presenter.py ├── requirements.txt ├── tarjan_route.log └── tests ├── test_data_loader.py ├── test_graph_utils.py ├── test_interface.py ├── test_logger_config.py ├── test_optimizer.py ├── test_presenter.py ├── test_utils.py └── test_main.py

markdown
Kopier kode

- **data/**: Contains the `routes.json` file with all route information.
- **modules/**: Houses all the modular components of the program.
  - `__init__.py`: Marks the directory as a Python package.
  - `data_loader.py`: Handles data parsing and loading.
  - `graph_utils.py`: Manages graph construction and related utilities.
  - `interface.py`: Facilitates user interaction and input handling.
  - `logger_config.py`: Configures the logging system.
  - `optimizer.py`: Contains optimization logic for route planning.
  - `presenter.py`: Manages the presentation of results to the user.
- **tests/**: Contains all unit test files for each module.
- **main.py**: The entry point of the program.
- **requirements.txt**: Lists all Python dependencies.
- **tarjan_route.log**: The log file generated during program execution.

## Prerequisites

- **Python 3.8 or higher**: Ensure that Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).
- **pip**: Python's package installer. It typically comes bundled with Python installations.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/tarjan_planner.git
   cd tarjan_planner
Create a Virtual Environment (Optional but Recommended)

bash
Kopier kode
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

Ensure you are in the project root directory (the directory containing requirements.txt).

bash
Kopier kode
pip install -r requirements.txt
Note: If you encounter issues with installing certain packages, ensure that you have the necessary build tools installed on your system.

Usage
Prepare the Route Data

Ensure that the data/routes.json file is populated with accurate route information. The provided structure should include all necessary attributes such as route names, positions, coordinates, travel modes, speeds, and costs.

Run the Program

Execute the main script to start the route optimization process.

bash
Kopier kode
python main.py
Select Optimization Criteria

Upon running, the program will prompt you to select your preferred optimization criterion:

markdown
Kopier kode
Select optimization criteria:
1. Shortest travel time
2. Least cost
3. Minimal number of transfers
Enter the number of your choice (1-3):
Enter 1, 2, or 3 based on your preference. If an invalid input is provided, the program defaults to optimizing for the shortest travel time.

View Results

After processing, the program will display the optimal path along with associated metrics such as total travel time, cost, or number of transfers. Additionally, a visual plot of the transport network highlighting the optimal route will be displayed.

Running Unit Tests
To ensure that all components of the program are functioning correctly, a suite of unit tests has been developed. These tests cover all modules and are essential for maintaining the program's integrity, especially after making changes or updates.

Navigate to the Project Root Directory

Ensure you are in the directory containing main.py and the modules/ and tests/ directories.

Run All Tests

Use Python's unittest discovery feature to automatically find and run all tests within the tests/ directory.

bash
Kopier kode
python -m unittest discover -s tests
Expected Output:

markdown
Kopier kode
........
----------------------------------------------------------------------
Ran 8 tests in 0.123s

OK
Run Individual Test Files

If you prefer to run tests individually, specify the test module name.

bash
Kopier kode
python -m unittest tests.test_data_loader
python -m unittest tests.test_graph_utils
python -m unittest tests.test_interface
python -m unittest tests.test_logger_config
python -m unittest tests.test_optimizer
python -m unittest tests.test_presenter
python -m unittest tests.test_utils
python -m unittest tests.test_main
Note: Ensure that you are executing these commands from the project root to maintain correct module paths.

Logging
The program utilizes a logging system to record significant events, warnings, and errors. All logs are written to the tarjan_route.log file located in the project root directory. This log file is essential for monitoring the program's execution and diagnosing issues.

Log Levels:

INFO: General information about the program's operations.
DEBUG: Detailed information useful for debugging.
ERROR: Errors encountered during execution.
Viewing Logs:

You can view the log file using any text editor or via the command line:

bash
Kopier kode
cat tarjan_route.log
Troubleshooting
1. ModuleNotFoundError: No module named 'modules'
Issue: When running unit tests, you encounter an error indicating that the modules package is not found.

Solution:

Ensure Proper Directory Structure: Verify that the modules/ directory contains an __init__.py file. This file marks the directory as a Python package, enabling proper module imports.

bash
Kopier kode
touch modules/__init__.py
Run Tests from Project Root: Always execute unit tests from the project's root directory to maintain correct module paths.

bash
Kopier kode
cd path/to/tarjan_planner
python -m unittest discover -s tests
Check PYTHONPATH: If issues persist, ensure that your Python environment includes the project root in the PYTHONPATH.

bash
Kopier kode
export PYTHONPATH=$PYTHONPATH:$(pwd)
2. Missing Dependencies
Issue: Errors related to missing Python packages during installation or execution.

Solution:

Install All Dependencies: Ensure that all required packages are installed via requirements.txt.

bash
Kopier kode
pip install -r requirements.txt
Verify Installation: Check that all packages listed in requirements.txt are successfully installed.

3. Malformed routes.json
Issue: The program fails to parse routes.json due to invalid JSON syntax.

Solution:

Validate JSON Syntax: Use online tools like JSONLint to validate the syntax of your routes.json file.
Ensure All Required Fields: Confirm that each route entry contains all necessary attributes.
4. Graph Construction Issues
Issue: The program generates incorrect graphs, leading to inaccurate optimization results.

Solution:

Verify Route Data: Ensure that all routes in routes.json are correctly defined with accurate coordinates and connections.
Review Logs: Check tarjan_route.log for any warnings or errors related to graph construction.
Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, please open an issue or submit a pull request.

Fork the Repository

Create a Feature Branch

bash
Kopier kode
git checkout -b feature/your-feature-name
Commit Your Changes

bash
Kopier kode
git commit -m "Add feature X"
Push to the Branch

bash
Kopier kode
git push origin feature/your-feature-name
Open a Pull Request

License
This project is licensed under the MIT License.