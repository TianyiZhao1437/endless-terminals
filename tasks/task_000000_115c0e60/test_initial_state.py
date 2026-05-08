# test_initial_state.py
import os
import pytest

DATAPIPELINE_DIR = "/home/user/datapipeline"
PROCESS_SCRIPT = os.path.join(DATAPIPELINE_DIR, "process_data.sh")
INPUT_FILE = os.path.join(DATAPIPELINE_DIR, "input.txt")
OUTPUT_FILE = os.path.join(DATAPIPELINE_DIR, "output.txt")
ERROR_LOG = os.path.join(DATAPIPELINE_DIR, "error.log")

def test_datapipeline_directory_does_not_exist():
    """
    At task start, the /home/user/datapipeline directory must NOT exist.
    """
    assert not os.path.exists(DATAPIPELINE_DIR), (
        f"Directory '{DATAPIPELINE_DIR}' already exists. "
        "Please start with a clean state: this directory should not exist before beginning the task."
    )

@pytest.mark.skip(reason="Artifacts should NOT exist before task start.")
def test_process_data_sh_does_not_exist():
    """
    process_data.sh should not exist before the task is started.
    """
    assert not os.path.exists(PROCESS_SCRIPT), (
        f"File '{PROCESS_SCRIPT}' already exists. "
        "Please ensure the script does not exist before starting the task."
    )

@pytest.mark.skip(reason="Artifacts should NOT exist before task start.")
def test_input_txt_does_not_exist():
    """
    input.txt should not exist before the task is started.
    """
    assert not os.path.exists(INPUT_FILE), (
        f"File '{INPUT_FILE}' already exists. "
        "Please ensure the input file does not exist before starting the task."
    )

@pytest.mark.skip(reason="Artifacts should NOT exist before task start.")
def test_output_txt_does_not_exist():
    """
    output.txt should not exist before the task is started.
    """
    assert not os.path.exists(OUTPUT_FILE), (
        f"File '{OUTPUT_FILE}' already exists. "
        "Please ensure the output file does not exist before starting the task."
    )

@pytest.mark.skip(reason="Artifacts should NOT exist before task start.")
def test_error_log_does_not_exist():
    """
    error.log should not exist before the task is started.
    """
    assert not os.path.exists(ERROR_LOG), (
        f"File '{ERROR_LOG}' already exists. "
        "Please ensure the error log does not exist before starting the task."
    )