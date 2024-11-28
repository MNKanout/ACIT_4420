# tests/test_sorter.py
import sys
import os
import shutil
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sorter import organize_files
from errors import DirectoryNotFoundError, PermissionDeniedError

def setup_test_environment(source_dir, files):
    os.makedirs(source_dir, exist_ok=True)
    for file in files:
        open(os.path.join(source_dir, file), 'a').close()

def teardown_test_environment(dirs):
    for dir in dirs:
        if os.path.exists(dir):
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
        assert os.path.exists(os.path.join(dest_dir, 'Others', 'data.csv'))
    finally:
        teardown_test_environment([source_dir, dest_dir])

def test_nonexistent_source_dir():
    with pytest.raises(DirectoryNotFoundError):
        organize_files('nonexistent_dir', 'dest_dir')

def test_permission_denied(mocker):
    source_dir = 'test_source'
    dest_dir = 'test_dest'
    files = ['test1.txt']
    setup_test_environment(source_dir, files)

    mocker.patch('shutil.move', side_effect=PermissionError)

    with pytest.raises(PermissionDeniedError):
        organize_files(source_dir, dest_dir)

    teardown_test_environment([source_dir, dest_dir])
