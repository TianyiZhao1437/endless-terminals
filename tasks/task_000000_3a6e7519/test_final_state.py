# test_final_state.py

import os
import pytest

LOG_PATH = "/home/user/python_version.log"

def get_python3_version():
    """
    Returns the version string of python3, e.g., '3.9.13'.
    Returns None if python3 is not installed.
    """
    import subprocess

    try:
        # Try to get version from 'python3 --version'
        # This outputs to stderr on some systems, so capture both
        result = subprocess.run(
            ["python3", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        if not output.startswith("Python 3"):
            return None
        # Output: 'Python 3.X.Y'
        parts = output.split()
        if len(parts) == 3 and parts[0] == "Python" and parts[1].startswith("3"):
            return parts[1]
        else:
            return None
    except FileNotFoundError:
        return None

@pytest.mark.final_state
def test_python_version_log_exists():
    """
    Validates that the log file exists after the task is completed.
    """
    assert os.path.isfile(LOG_PATH), (
        f"The log file '{LOG_PATH}' does not exist. "
        "You must create this file as part of the task."
    )

@pytest.mark.final_state
def test_python_version_log_contents():
    """
    Validates the contents of /home/user/python_version.log after the task is completed.
    Ensures it matches the exact required output and formatting.
    """
    assert os.path.isfile(LOG_PATH), (
        f"The log file '{LOG_PATH}' does not exist. "
        "You must create this file as part of the task."
    )

    with open(LOG_PATH, "rb") as f:
        content_bytes = f.read()

    # Ensure there are no extra bytes (e.g., no BOM, no extra lines)
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(
            f"The log file '{LOG_PATH}' is not valid UTF-8 text. "
            "Please ensure it is a plain text file."
        )

    # The file must end with exactly one newline, and have only one line
    if content == "":
        pytest.fail(
            f"The log file '{LOG_PATH}' is empty. "
            "It must contain the required output as a single line."
        )
    if not content.endswith('\n'):
        pytest.fail(
            f"The log file '{LOG_PATH}' does not end with a newline character. "
            "It must end with exactly one '\\n'."
        )
    lines = content.splitlines(keepends=False)
    if len(lines) != 1:
        pytest.fail(
            f"The log file '{LOG_PATH}' contains {len(lines)} lines. "
            "It must contain exactly one line."
        )

    line = lines[0]

    # There must be no leading or trailing whitespace
    if line.strip() != line:
        pytest.fail(
            f"The log file '{LOG_PATH}' contains leading or trailing whitespace: {repr(line)}. "
            "There must be no extra whitespace before or after the line."
        )

    # Determine the expected content
    version = get_python3_version()
    if version is not None:
        expected_line = f"Python {version} installed"
    else:
        expected_line = "No Python 3 installed"

    if line != expected_line:
        pytest.fail(
            f"The log file '{LOG_PATH}' contains incorrect content.\n"
            f"Expected: '{expected_line}'\n"
            f"Found:    '{line}'\n"
            "Ensure the file contains exactly the required output, "
            "with the correct Python 3 version if installed, "
            "or 'No Python 3 installed' if not."
        )