# test_final_state.py
"""
Pytest suite to validate the FINAL state after completion of the 'datapipeline' task.

Checks:
- Directory /home/user/datapipeline exists.
- Files:
    * process_data.sh (executable)
    * input.txt with correct content
    * output.txt with correct content
- error.log does NOT exist
- process_data.sh logic (not tested here, but its effect is validated)
"""

import os
import stat
import pytest

DATAPIPELINE_DIR = "/home/user/datapipeline"
PROCESS_SCRIPT = os.path.join(DATAPIPELINE_DIR, "process_data.sh")
INPUT_FILE = os.path.join(DATAPIPELINE_DIR, "input.txt")
OUTPUT_FILE = os.path.join(DATAPIPELINE_DIR, "output.txt")
ERROR_LOG = os.path.join(DATAPIPELINE_DIR, "error.log")

EXPECTED_INPUT = [
    "apple",
    "Banana",
    "cHeRry"
]

EXPECTED_OUTPUT = [
    "APPLE",
    "BANANA",
    "CHERRY"
]

def test_datapipeline_directory_exists():
    """
    /home/user/datapipeline must exist after task completion.
    """
    assert os.path.isdir(DATAPIPELINE_DIR), (
        f"Expected directory '{DATAPIPELINE_DIR}' does not exist. "
        "Create this directory as specified."
    )

def test_process_data_sh_exists_and_executable():
    """
    process_data.sh must exist and be executable.
    """
    assert os.path.isfile(PROCESS_SCRIPT), (
        f"Expected script '{PROCESS_SCRIPT}' does not exist. "
        "Create this file inside the datapipeline directory."
    )
    st = os.stat(PROCESS_SCRIPT)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, (
        f"Script '{PROCESS_SCRIPT}' exists but is not executable. "
        "Set executable permissions (chmod +x) on this script."
    )

def test_input_txt_exists_and_content():
    """
    input.txt must exist and contain the correct content.
    """
    assert os.path.isfile(INPUT_FILE), (
        f"Expected input file '{INPUT_FILE}' does not exist. "
        "Create this file with the specified content."
    )
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == EXPECTED_INPUT, (
        f"Content of '{INPUT_FILE}' is incorrect.\n"
        f"Expected:\n{EXPECTED_INPUT}\nFound:\n{lines}\n"
        "Ensure the file contains exactly these lines, one per line, with no extra whitespace."
    )

def test_output_txt_exists_and_content():
    """
    output.txt must exist and contain the uppercase versions of input.txt, one per line, no extra whitespace.
    """
    assert os.path.isfile(OUTPUT_FILE), (
        f"Expected output file '{OUTPUT_FILE}' does not exist. "
        "Run the script to generate this file."
    )
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n').strip() for line in f]
    assert lines == EXPECTED_OUTPUT, (
        f"Content of '{OUTPUT_FILE}' is incorrect.\n"
        f"Expected:\n{EXPECTED_OUTPUT}\nFound:\n{lines}\n"
        "Ensure each line is the uppercase version of the corresponding line in input.txt, "
        "with no leading/trailing whitespace, and no extra lines."
    )

def test_error_log_not_present():
    """
    error.log must NOT exist after a successful run (input.txt present).
    """
    assert not os.path.exists(ERROR_LOG), (
        f"Error log '{ERROR_LOG}' exists but should NOT be present after a successful script run with input.txt. "
        "Remove this file if input.txt was processed successfully."
    )

def test_datapipeline_directory_contents_exact():
    """
    /home/user/datapipeline must contain ONLY process_data.sh, input.txt, output.txt after a successful run.
    (error.log must not exist, no extra files)
    """
    expected_files = {"process_data.sh", "input.txt", "output.txt"}
    actual_files = set(os.listdir(DATAPIPELINE_DIR))
    missing = expected_files - actual_files
    extra = actual_files - expected_files
    assert not missing, (
        f"Missing required files in '{DATAPIPELINE_DIR}': {missing}. "
        "Ensure all required files are present."
    )
    assert not extra, (
        f"Unexpected extra files in '{DATAPIPELINE_DIR}': {extra}. "
        "Remove any files not specified in the task requirements."
    )