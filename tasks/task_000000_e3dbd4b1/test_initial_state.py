# test_initial_state.py

import os
import pytest

CONTAINERS_DIR = "/home/user/project/data/containers"
SIF_FILES = [
    "modelA_v1.sif",
    "data_preprocessor.sif",
    "modelB_v2.sif",
]
CONTAINER_LIST_FILE = "/home/user/project/container_list.txt"

def test_containers_dir_exists_and_is_dir():
    assert os.path.exists(CONTAINERS_DIR), (
        f"Directory {CONTAINERS_DIR} does not exist. "
        "Expected directory with .sif files before starting the task."
    )
    assert os.path.isdir(CONTAINERS_DIR), (
        f"{CONTAINERS_DIR} exists but is not a directory."
    )

@pytest.mark.parametrize("filename", SIF_FILES)
def test_each_sif_file_exists(filename):
    full_path = os.path.join(CONTAINERS_DIR, filename)
    assert os.path.isfile(full_path), (
        f"Missing required .sif file: {full_path}. "
        "All specified .sif files must exist before the task."
    )

def test_no_extra_files_in_containers_dir():
    files = [
        f for f in os.listdir(CONTAINERS_DIR)
        if os.path.isfile(os.path.join(CONTAINERS_DIR, f))
    ]
    sif_files_set = set(SIF_FILES)
    actual_sif_files_set = {f for f in files if f.endswith(".sif")}
    assert actual_sif_files_set == sif_files_set, (
        f"Expected only these .sif files in {CONTAINERS_DIR}: {sorted(sif_files_set)}\n"
        f"Found: {sorted(actual_sif_files_set)}"
    )

def test_container_list_file_does_not_exist():
    assert not os.path.exists(CONTAINER_LIST_FILE), (
        f"{CONTAINER_LIST_FILE} already exists before the task. "
        "It should be created by the agent."
    )