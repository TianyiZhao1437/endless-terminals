# test_initial_state.py

import os
import pytest

HOME = "/home/user"
PROJECTS = os.path.join(HOME, "projects")
ARCHIVES = os.path.join(HOME, "archives")

alpha_dir = os.path.join(PROJECTS, "alpha_data")
beta_dir = os.path.join(PROJECTS, "beta_data")

alpha_file = os.path.join(alpha_dir, "file_a.txt")
alpha_config = os.path.join(alpha_dir, "config_a.yaml")
beta_file = os.path.join(beta_dir, "file_b.txt")
beta_config = os.path.join(beta_dir, "config_b.yaml")

def read_file(path):
    with open(path, "r") as f:
        return f.read().strip()

@pytest.mark.parametrize("path", [
    alpha_dir,
    beta_dir,
])
def test_project_directories_exist(path):
    assert os.path.isdir(path), f"Missing directory: {path}"

@pytest.mark.parametrize("path,expected", [
    (alpha_file, "Alpha file content"),
    (alpha_config, "alpha: config"),
    (beta_file, "Beta file content"),
    (beta_config, "beta: config"),
])
def test_project_files_exist_and_content(path, expected):
    assert os.path.isfile(path), f"Missing file: {path}"
    content = read_file(path)
    assert content == expected, f"File at {path} has incorrect content. Expected: '{expected}', Found: '{content}'"

def test_archives_directory_exists_and_writable():
    assert os.path.isdir(ARCHIVES), f"Missing archives directory: {ARCHIVES}"
    # Test writable by creating and deleting a temp file
    temp_file = os.path.join(ARCHIVES, ".pytest_write_test")
    try:
        with open(temp_file, "w") as f:
            f.write("test")
    except Exception as e:
        pytest.fail(f"Cannot write to archives directory: {ARCHIVES}. Error: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)