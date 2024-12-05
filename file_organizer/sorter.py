# sorter.py

import os
import shutil
import re
from logger import setup_logger
from errors import DirectoryNotFoundError, PermissionDeniedError
from filetype_handlers import file_type_registry

def organize_files(source_dir, dest_base_dir):
    logger = setup_logger()

    if not os.path.exists(source_dir):
        logger.error(f"Source directory {source_dir} does not exist.")
        raise DirectoryNotFoundError(f"Source directory {source_dir} does not exist.")

    if not os.path.exists(dest_base_dir):
        logger.info(f"Destination directory {dest_base_dir} does not exist. Creating it.")
        os.makedirs(dest_base_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            matched = False
            for pattern, target_dir in file_type_registry:
                if pattern.search(file):
                    dest_dir = os.path.join(dest_base_dir, target_dir)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    try:
                        shutil.move(file_path, dest_dir)
                        logger.info(f"Moved file {file_path} to {dest_dir}")
                    except PermissionError as e:
                        logger.error(f"Permission error moving file {file_path}: {e}")
                        raise PermissionDeniedError(f"Permission error moving file {file_path}: {e}")
                    matched = True
                    break
            if not matched:
                # Move to 'Others' directory
                dest_dir = os.path.join(dest_base_dir, 'Others')
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                try:
                    shutil.move(file_path, dest_dir)
                    logger.info(f"Moved file {file_path} to {dest_dir}")
                except PermissionError as e:
                    logger.error(f"Permission error moving file {file_path}: {e}")
                    raise PermissionDeniedError(f"Permission error moving file {file_path}: {e}")
