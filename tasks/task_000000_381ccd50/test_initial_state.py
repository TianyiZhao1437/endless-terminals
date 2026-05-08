# test_initial_state.py

import pytest
import os

CONF_PATH = "/home/user/mlops/artifact_service.conf"
EXPECTED_INITIAL_CONTENT = "artifact_dir=/tmp/some/old/path"

def test_artifact_service_conf_exists():
    """Check that the artifact_service.conf file exists before the task."""
    assert os.path.isfile(CONF_PATH), (
        f"Missing file: {CONF_PATH}. "
        "You must create this configuration file before proceeding."
    )

def test_artifact_service_conf_initial_content():
    """Check that artifact_service.conf contains the expected initial content."""
    with open(CONF_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    artifact_dir_lines = [line for line in lines if line.startswith("artifact_dir=")]
    assert artifact_dir_lines, (
        f"{CONF_PATH} must contain a line starting with 'artifact_dir='. "
        "Add the correct line before proceeding."
    )
    assert artifact_dir_lines[0] == EXPECTED_INITIAL_CONTENT, (
        f"{CONF_PATH} should initially contain:\n{EXPECTED_INITIAL_CONTENT}\n"
        f"but found:\n{artifact_dir_lines[0]}\n"
        "Update the configuration file to match the required initial state."
    )