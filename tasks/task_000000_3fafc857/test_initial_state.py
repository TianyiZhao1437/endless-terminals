# test_initial_state.py

import os
import pytest

LOG_FILE = "/home/user/process_investigation.log"
EXPECTED_CONTENT = (
    "PID,USER,COMMAND,%MEM\n"
    "382,user,firefox,12.88\n"
    "1893,user,python3,6.17\n"
    "443,user,code,4.78\n"
)

def test_log_file_does_not_exist():
    """The process investigation log file should not exist before the investigation is performed."""
    assert not os.path.exists(LOG_FILE), (
        f"The log file '{LOG_FILE}' should NOT exist before you perform the investigation. "
        "Please do not create the output file before completing the required steps."
    )

@pytest.mark.parametrize("path", [
    "/home/user/firefox",
    "/home/user/python3",
    "/home/user/code",
])
def test_output_files_do_not_exist(path):
    """No output files or directories related to the expected processes should exist yet."""
    assert not os.path.exists(path), (
        f"The file or directory '{path}' should NOT exist before you perform the investigation. "
        "Only the log file in the correct format should be created after the task."
    )