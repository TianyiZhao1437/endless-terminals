# test_final_state.py

import os
import pytest

CONTAINERS_DIR = "/home/user/project/data/containers"
SIF_FILES = [
    "modelA_v1.sif",
    "data_preprocessor.sif",
    "modelB_v2.sif",
]
EXPECTED_LIST_FILE = "/home/user/project/container_list.txt"
EXPECTED_LIST_CONTENT = "data_preprocessor.sif\nmodelA_v1.sif\nmodelB_v2.sif\n"

def test_container_list_file_exists():
    assert os.path.exists(EXPECTED_LIST_FILE), (
        f"{EXPECTED_LIST_FILE} does not exist. "
        "You must create this file containing the sorted list of container image filenames."
    )
    assert os.path.isfile(EXPECTED_LIST_FILE), (
        f"{EXPECTED_LIST_FILE} exists but is not a regular file."
    )

def test_container_list_file_content_exact():
    assert os.path.isfile(EXPECTED_LIST_FILE), (
        f"{EXPECTED_LIST_FILE} does not exist as a file."
    )
    with open(EXPECTED_LIST_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LIST_CONTENT, (
        f"{EXPECTED_LIST_FILE} content is incorrect.\n"
        f"Expected exactly (including line breaks):\n"
        f"---\n{EXPECTED_LIST_CONTENT}---\n"
        f"Found:\n"
        f"---\n{content}---"
    )

def test_container_list_file_no_extra_lines():
    with open(EXPECTED_LIST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    expected_lines = [
        "data_preprocessor.sif\n",
        "modelA_v1.sif\n",
        "modelB_v2.sif\n",
    ]
    assert lines == expected_lines, (
        f"{EXPECTED_LIST_FILE} does not have the correct number of lines or correct line endings.\n"
        f"Expected lines:\n{expected_lines!r}\n"
        f"Found lines:\n{lines!r}"
    )

def test_container_list_file_no_extra_whitespace():
    with open(EXPECTED_LIST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        stripped = line.rstrip('\n')
        assert stripped == stripped.strip(), (
            f"Line {i+1} in {EXPECTED_LIST_FILE} contains unexpected leading/trailing whitespace: {repr(line)}"
        )

def test_container_list_file_has_only_sif_filenames():
    with open(EXPECTED_LIST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    actual_filenames = [line.rstrip('\n') for line in lines if line.strip() != ""]
    for fn in actual_filenames:
        assert fn in SIF_FILES, (
            f"{EXPECTED_LIST_FILE} contains unexpected filename: {fn!r} "
            f"(should only list the .sif files present in {CONTAINERS_DIR})"
        )
        assert os.path.sep not in fn, (
            f"{EXPECTED_LIST_FILE} contains a path instead of just a filename: {fn!r}"
        )

def test_container_list_file_sorted():
    with open(EXPECTED_LIST_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f if line.strip() != ""]
    expected_sorted = sorted(SIF_FILES)
    assert lines == expected_sorted, (
        f"{EXPECTED_LIST_FILE} is not sorted alphabetically by filename.\n"
        f"Expected order: {expected_sorted}\n"
        f"Found: {lines}"
    )

def test_container_list_file_empty_if_no_sif_files(monkeypatch, tmp_path):
    # Simulate the "no .sif files" case
    empty_containers_dir = tmp_path / "containers"
    empty_containers_dir.mkdir(parents=True, exist_ok=True)
    simulated_list_file = tmp_path / "container_list.txt"
    # Simulate agent's logic: list .sif files, write to output file
    sif_files = [f for f in os.listdir(empty_containers_dir) if f.endswith(".sif")]
    with open(simulated_list_file, "w", encoding="utf-8") as f:
        for sif in sorted(sif_files):
            f.write(f"{sif}\n")
    with open(simulated_list_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "", (
        "If there are no .sif files, the output file must be empty, but it contains:\n"
        f"{content!r}"
    )