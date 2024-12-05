# File Organizer

A Python-based tool to organize files in a directory based on their file types.

## Features

- Automatically categorizes files (e.g., TextFiles, Images, Music).
- Supports plugins for custom file types.
- Handles nested directories, hidden files, and special characters in filenames.
- Robust error handling for permissions and missing directories.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/file-organizer.git
   cd file-organizer


2. Create a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies:

3. Install dependencies
pip install -r requirements.txt
(Optional) Create a config.json file to customize directory mappings.

Usage
Run the program:

python main.py <source_directory> <destination_directory>
Example:

python main.py ~/Downloads ~/OrganizedFiles

Add plugins:

Place custom plugin files in the plugins/ folder.
Use the @register_file_type decorator in plugins to define new file type patterns.
View logs:

Check file_organizer.log for detailed logs of operations.