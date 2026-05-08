# test_final_state.py

import os
import pytest

OUTPUT_FILE = "/home/user/docs/legacy_greet_output.txt"
EXPECTED_OUTPUT = "Greeting from the legacy script:\nHello, World!\n"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"The output file does not exist at: {OUTPUT_FILE}"
    )

def test_output_file_is_readable():
    assert os.access(OUTPUT_FILE, os.R_OK), (
        f"The output file at {OUTPUT_FILE} is not readable by user."
    )

def test_output_file_content_exactness():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            actual_content = f.read()
    except Exception as e:
        pytest.fail(
            f"Could not read {OUTPUT_FILE}: {e}"
        )

    if actual_content != EXPECTED_OUTPUT:
        # Show differences for easier debugging
        from difflib import unified_diff
        diff = '\n'.join(unified_diff(
            EXPECTED_OUTPUT.splitlines(keepends=True),
            actual_content.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual"
        ))
        pytest.fail(
            f"The content of {OUTPUT_FILE} does not match the expected output.\n"
            f"Expected (repr): {repr(EXPECTED_OUTPUT)}\n"
            f"Actual   (repr): {repr(actual_content)}\n"
            f"Diff:\n{diff}\n"
            "Check for missing/extra lines, incorrect whitespace, or wrong line endings."
        )