# main.py

import sys
from sorter import organize_files
from config import load_config
from logger import setup_logger
import os
import importlib.util

def load_plugins(plugins_dir='plugins'):
    if not os.path.exists(plugins_dir):
        return
    for filename in os.listdir(plugins_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(plugins_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

def main():
    logger = setup_logger()

    # Load configuration
    config = load_config()

    # Load plugins
    load_plugins()

    if len(sys.argv) < 3:
        logger.error("Usage: python main.py <source_directory> <destination_base_directory>")
        sys.exit(1)

    source_dir = sys.argv[1]
    dest_base_dir = sys.argv[2]

    try:
        organize_files(source_dir, dest_base_dir)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
