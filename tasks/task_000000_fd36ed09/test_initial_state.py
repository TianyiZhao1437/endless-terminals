# test_initial_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/scripts/legacy_greet.sh"
DOCS_DIR = "/home/user/docs"

LEGACY_SCRIPT_CONTENT = (
    "#!/bin/bash\n"
    "echo \"Greeting from the legacy script:\"\n"
    "echo \"Hello, $1!\"\n"
)

def test_legacy_greet_script_exists_and_is_executable_and_contents():
    assert os.path.isfile(SCRIPT_PATH), (
        f"Required script does not exist at: {SCRIPT_PATH}"
    )
    # Check readable
    assert os.access(SCRIPT_PATH, os.R_OK), (
        f"Script at {SCRIPT_PATH} is not readable."
    )
    # Check executable
    assert os.access(SCRIPT_PATH, os.X_OK), (
        f"Script at {SCRIPT_PATH} is not executable."
    )
    # Check contents
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != LEGACY_SCRIPT_CONTENT:
        actual_repr = repr(actual)
        expected_repr = repr(LEGACY_SCRIPT_CONTENT)
        pytest.fail(
            f"The contents of {SCRIPT_PATH} do not match the expected script.\n"
            f"Expected:\n{expected_repr}\nActual:\n{actual_repr}"
        )

def test_docs_directory_exists_and_is_writable():
    assert os.path.isdir(DOCS_DIR), (
        f"Docs directory does not exist at: {DOCS_DIR}"
    )
    # Check writable
    assert os.access(DOCS_DIR, os.W_OK), (
        f"Docs directory at {DOCS_DIR} is not writable."
    )