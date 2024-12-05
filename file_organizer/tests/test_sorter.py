# tests/test_sorter.py

import sys
import os
import shutil
from pathlib import Path
import pytest
from unittest.mock import patch

# Ensure the parent directory is in the import path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import load_plugins
from sorter import organize_files
from errors import DirectoryNotFoundError, PermissionDeniedError

def setup_test_environment(source_dir, files):
    os.makedirs(source_dir, exist_ok=True)
    for file in files:
        # Create directories if specified
        if os.sep in file:
            os.makedirs(os.path.join(source_dir, os.path.dirname(file)), exist_ok=True)
        open(os.path.join(source_dir, file), 'a').close()

def teardown_test_environment(dirs):
    for dir in dirs:
        if os.path.exists(dir):
            # Handle read-only files and directories
            for root, dirs_in_root, files_in_root in os.walk(dir, topdown=False):
                for name in files_in_root:
                    filepath = os.path.join(root, name)
                    try:
                        os.chmod(filepath, 0o777)
                    except FileNotFoundError:
                        pass  # File might have been deleted already
                for name in dirs_in_root:
                    dirpath = os.path.join(root, name)
                    try:
                        os.chmod(dirpath, 0o777)
                    except FileNotFoundError:
                        pass  # Directory might have been deleted already
            shutil.rmtree(dir)


def test_organize_files():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['test1.txt', 'image1.jpg', 'doc1.pdf', 'song.mp3', 'data.csv']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'test1.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'Images', 'image1.jpg'))
        assert os.path.exists(os.path.join(dest_dir, 'PDFs', 'doc1.pdf'))
        assert os.path.exists(os.path.join(dest_dir, 'Music', 'song.mp3'))
        # 'data.csv' should go to 'Spreadsheets' if custom_types.py is loaded
        assert os.path.exists(os.path.join(dest_dir, 'Spreadsheets', 'data.csv')) or \
               os.path.exists(os.path.join(dest_dir, 'Others', 'data.csv'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_nonexistent_source_dir():
    with pytest.raises(DirectoryNotFoundError):
        organize_files('nonexistent_dir', 'dest_dir')

def test_permission_denied():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['test1.txt']
    setup_test_environment(source_dir, files)

    with patch('shutil.move', side_effect=PermissionError), \
         pytest.raises(PermissionDeniedError):
        organize_files(source_dir, dest_dir)

    teardown_test_environment([source_dir, dest_dir])

def test_hidden_files():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['.hiddenfile', '.hiddenfolder/hiddenfile.txt']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        # Hidden files should be moved to 'Others' unless matched by a pattern
        assert os.path.exists(os.path.join(dest_dir, 'Others', '.hiddenfile'))
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'hiddenfile.txt'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_files_without_extension():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['README', 'LICENSE']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        # Files without extensions should go to 'Others'
        assert os.path.exists(os.path.join(dest_dir, 'Others', 'README'))
        assert os.path.exists(os.path.join(dest_dir, 'Others', 'LICENSE'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_nested_directories():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['folder1/file1.txt', 'folder2/subfolder/file2.jpg']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'file1.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'Images', 'file2.jpg'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_special_characters_in_filenames():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['test @#$%.txt', 'uniçodê😊.jpg']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'test @#$%.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'Images', 'uniçodê😊.jpg'))
    finally:
        teardown_test_environment([source_dir, dest_dir])


def test_read_only_files():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['readonly.txt']
    setup_test_environment(source_dir, files)

    # Make the file read-only
    os.chmod(os.path.join(source_dir, 'readonly.txt'), 0o444)

    try:
        organize_files(source_dir, dest_dir)
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'readonly.txt'))
    finally:
        # Reset permissions to delete the file
        os.chmod(os.path.join(dest_dir, 'TextFiles', 'readonly.txt'), 0o666)
        teardown_test_environment([source_dir, dest_dir])


def test_large_number_of_files():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = [f'file_{i}.txt' for i in range(100)]  # Adjust the number if needed
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        for file in files:
            assert os.path.exists(os.path.join(dest_dir, 'TextFiles', file))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_files_are_moved_not_copied():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['test1.txt']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        # Check file exists in destination
        assert os.path.exists(os.path.join(dest_dir, 'TextFiles', 'test1.txt'))
        # Check file does not exist in source
        assert not os.path.exists(os.path.join(source_dir, 'test1.txt'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_empty_directories_left_behind():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['folder1/file1.txt']
    setup_test_environment(source_dir, files)

    try:
        organize_files(source_dir, dest_dir)
        # After moving files, empty directories should be left behind
        assert os.path.exists(os.path.join(source_dir, 'folder1'))
        assert not os.listdir(os.path.join(source_dir, 'folder1'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_custom_file_type_from_plugin():
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['document.docx']
    setup_test_environment(source_dir, files)

    # Load plugins to register custom file types
    load_plugins()

    try:
        organize_files(source_dir, dest_dir)
        # Check if the file is moved to 'Documents' directory from plugin
        assert os.path.exists(os.path.join(dest_dir, 'Documents', 'document.docx'))
    finally:
        teardown_test_environment([source_dir, dest_dir])
