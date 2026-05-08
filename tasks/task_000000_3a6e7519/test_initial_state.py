# test_initial_state.py

import os
import subprocess
import pytest

LOG_PATH = "/home/user/python_version.log"

def get_python3_version():
    """
    Returns the version string of python3, e.g., '3.9.13'.
    Returns None if python3 is not installed.
    """
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

@pytest.mark.initial_state
def test_python_version_log_absent():
    """
    Validates that the log file does NOT exist before the student performs the task.
    """
    assert not os.path.exists(LOG_PATH), (
        f"The log file '{LOG_PATH}' should not exist yet. "
        "Please perform the task before checking for its existence."
    )

@pytest.mark.initial_state
def test_python3_installed():
    """
    Validates that Python 3 is installed (for the initial state).
    If not installed, that's fine for the initial state.
    """
    version = get_python3_version()
    # No assertion: just report for info
    if version is None:
        pytest.skip("Python 3 is not installed. This may be expected for the initial state.")
    else:
        # Check version is at least 3.8
        major_minor = tuple(int(x) for x in version.split('.')[:2])
        assert major_minor >= (3, 8), (
            f"Python 3 is installed, but version is {version}. "
            "Version must be at least 3.8 for compatibility."
        )