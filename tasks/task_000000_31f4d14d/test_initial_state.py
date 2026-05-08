# test_initial_state.py

import os
import pytest
import shutil

BINARY_PATH = "/home/user/builds/myapp"
SCAN_TOOL = "echo"
EXPECTED_SCAN_OUTPUT = "No vulnerabilities found in /home/user/builds/myapp"

@pytest.mark.parametrize("path", [
    BINARY_PATH,
])
def test_myapp_binary_exists_and_readable(path):
    assert os.path.isfile(path), (
        f"Required binary '{path}' does not exist as a file. "
        "Please ensure the application has been compiled to this location."
    )
    assert os.access(path, os.R_OK), (
        f"Required binary '{path}' is not readable. "
        "Ensure permissions allow read access."
    )

def test_scan_tool_echo_available():
    echo_path = shutil.which(SCAN_TOOL)
    assert echo_path is not None, (
        f"The scan tool '{SCAN_TOOL}' is not available on the system PATH. "
        "Please ensure it is installed and accessible."
    )

def test_echo_scan_command_produces_expected_output():
    import subprocess

    result = subprocess.run(
        [SCAN_TOOL, EXPECTED_SCAN_OUTPUT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"Running '{SCAN_TOOL} {EXPECTED_SCAN_OUTPUT}' failed with return code {result.returncode}."
    )
    output = result.stdout.strip()
    assert output == EXPECTED_SCAN_OUTPUT, (
        f"Expected '{EXPECTED_SCAN_OUTPUT}' as scan output, but got '{output}'."
    )