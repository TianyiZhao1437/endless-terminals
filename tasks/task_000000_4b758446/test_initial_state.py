# test_initial_state.py

import os
import pytest

CONFIG_V1_PATH = "/home/user/configs/config_v1.conf"
CONFIG_V2_PATH = "/home/user/configs/config_v2.conf"
CHANGES_LOG_PATH = "/home/user/config_changes.log"
CONFIGS_DIR = "/home/user/configs"

CONFIG_V1_CONTENT = """server.host=localhost
server.port=8080
database.url=jdbc:mysql://localhost/db
log.level=info
"""

CONFIG_V2_CONTENT = """server.host=localhost
server.port=8080
database.url=jdbc:mysql://localhost/db
log.level=info
server.port=8081
log.level=debug
"""

@pytest.mark.parametrize("path", [CONFIGS_DIR])
def test_configs_directory_exists(path):
    assert os.path.isdir(path), f"Required directory '{path}' does not exist."

@pytest.mark.parametrize("path,expected", [
    (CONFIG_V1_PATH, CONFIG_V1_CONTENT),
    (CONFIG_V2_PATH, CONFIG_V2_CONTENT),
])
def test_config_files_exist_with_expected_content(path, expected):
    assert os.path.isfile(path), f"Required file '{path}' does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize line endings for comparison
    norm_content = content.replace('\r\n', '\n').replace('\r', '\n')
    norm_expected = expected.replace('\r\n', '\n').replace('\r', '\n')
    assert norm_content == norm_expected, (
        f"File '{path}' exists but does not have the expected contents.\n"
        f"Expected:\n{norm_expected}\nActual:\n{norm_content}"
    )

def test_config_changes_log_does_not_exist_yet():
    assert not os.path.exists(CHANGES_LOG_PATH), (
        f"Output file '{CHANGES_LOG_PATH}' should not exist before the task is performed."
    )