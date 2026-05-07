# test_final_state.py

import os
import pytest
import subprocess

LOG_FILE = '/home/user/network-pip-packages.log'

def _get_pip_freeze_output():
    """
    Returns the output of `pip freeze` as a list of lines (stripped of newline).
    """
    try:
        # Run pip freeze in the current environment
        result = subprocess.run(
            ['pip', 'freeze'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        return lines
    except Exception as e:
        pytest.skip(f"Could not run pip freeze: {e}")

def test_log_file_exists():
    """
    The log file must exist after the task is completed.
    """
    assert os.path.exists(LOG_FILE), (
        f"The file {LOG_FILE} does not exist. "
        "You must create this file with the output of `pip freeze`."
    )

def test_log_file_is_regular_file():
    """
    The log file must be a regular file, not a directory or symlink.
    """
    assert os.path.isfile(LOG_FILE), (
        f"{LOG_FILE} exists but is not a regular file."
    )

def test_log_file_content_matches_pip_freeze():
    """
    The log file must contain exactly the output of `pip freeze` (no headers or extra text).
    """
    # Get expected pip freeze output
    expected_lines = _get_pip_freeze_output()

    # Read actual lines from the log file
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            actual_lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Could not read {LOG_FILE}: {e}")

    # Check exact match of contents (including order)
    assert actual_lines == expected_lines, (
        f"The contents of {LOG_FILE} do not match the output of `pip freeze`.\n"
        "Expected:\n"
        + ("\n".join(expected_lines) if expected_lines else "(empty file)")
        + "\nActual:\n"
        + ("\n".join(actual_lines) if actual_lines else "(empty file)")
        + "\n"
        "The file must contain ONLY the output of `pip freeze`, with no extra text, "
        "headers, or explanations. Each line must be in the form 'package==version'."
    )

def test_log_file_has_no_extra_lines():
    """
    The log file must not have any extra lines, explanations, or headers.
    """
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # All lines should either be blank or match pip freeze format
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '':
            continue  # empty lines are allowed only if pip freeze gives them
        # Check for proper pip freeze format: package==version
        if '==' not in stripped:
            pytest.fail(
                f"Line {idx+1} in {LOG_FILE} ('{stripped}') does not match the expected 'package==version' format. "
                "Remove any explanations, headers, or extra text."
            )
        pkg, version = stripped.split('==', 1)
        if not pkg or not version:
            pytest.fail(
                f"Line {idx+1} in {LOG_FILE} ('{stripped}') is not properly formatted as 'package==version'."
            )