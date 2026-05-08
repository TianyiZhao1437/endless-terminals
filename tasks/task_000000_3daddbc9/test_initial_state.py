# test_initial_state.py

import os
import stat
import pytest

ALERTS_DIR = '/home/user/alerts'
RULES_CONF = os.path.join(ALERTS_DIR, 'rules.conf')
PATCH_FILE = os.path.join(ALERTS_DIR, 'rules.conf.patch')
PATCH_OUTPUT_LOG = os.path.join(ALERTS_DIR, 'patch_output.log')

RULES_CONF_INITIAL_CONTENT = """[alert1]
name: High Memory Usage
threshold: 90
enabled: true

[alert2]
name: High CPU Load
threshold: 95
enabled: false
"""

RULES_CONF_PATCH_CONTENT = """--- rules.conf\t2023-06-10 10:00:00.000000000 +0000
+++ rules.conf\t2023-06-10 12:00:00.000000000 +0000
@@ -5,7 +5,8 @@

 [alert2]
 name: High CPU Load
-threshold: 95
-enabled: false
+threshold: 85
+enabled: true
"""

@pytest.mark.order(1)
def test_alerts_directory_exists():
    assert os.path.isdir(ALERTS_DIR), (
        f"Directory '{ALERTS_DIR}' is missing. "
        "Ensure you have created it before starting the task."
    )

@pytest.mark.order(2)
def test_alerts_directory_writable():
    # User must have write permission to alerts directory
    st = os.stat(ALERTS_DIR)
    mode = st.st_mode
    assert mode & stat.S_IWUSR, (
        f"Directory '{ALERTS_DIR}' is not writable by the user. "
        "Ensure you have the correct permissions."
    )

@pytest.mark.order(3)
def test_rules_conf_exists():
    assert os.path.isfile(RULES_CONF), (
        f"File '{RULES_CONF}' is missing. "
        "Ensure the original alert rules configuration file is present."
    )

@pytest.mark.order(4)
def test_rules_conf_content():
    with open(RULES_CONF, 'r', encoding='utf-8') as f:
        actual = f.read()
    assert actual == RULES_CONF_INITIAL_CONTENT, (
        f"File '{RULES_CONF}' does not have the expected initial content.\n"
        "If you have already applied the patch, please revert to the initial state.\n"
        "Expected content:\n"
        f"{RULES_CONF_INITIAL_CONTENT}\n"
        "Actual content:\n"
        f"{actual}"
    )

@pytest.mark.order(5)
def test_patch_file_exists():
    assert os.path.isfile(PATCH_FILE), (
        f"Patch file '{PATCH_FILE}' is missing. "
        "Ensure the patch file is present in the alerts directory."
    )

@pytest.mark.order(6)
def test_patch_file_content():
    with open(PATCH_FILE, 'r', encoding='utf-8') as f:
        actual = f.read()
    # Normalize line endings for robust comparison
    expected = PATCH_FILE_CONTENT_NORMALIZED(RULES_CONF_PATCH_CONTENT)
    actual_normalized = PATCH_FILE_CONTENT_NORMALIZED(actual)
    assert actual_normalized == expected, (
        f"Patch file '{PATCH_FILE}' content does not match expected patch.\n"
        "Expected content:\n"
        f"{RULES_CONF_PATCH_CONTENT}\n"
        "Actual content:\n"
        f"{actual}"
    )

@pytest.mark.order(7)
def test_patch_output_log_does_not_exist():
    assert not os.path.exists(PATCH_OUTPUT_LOG), (
        f"File '{PATCH_OUTPUT_LOG}' already exists. "
        "You should start from the initial state, before running the patch. "
        "Remove this file before proceeding."
    )


def PATCH_FILE_CONTENT_NORMALIZED(s):
    # Normalize tabs, line endings, and trailing newlines for comparison
    return s.replace('\r\n', '\n').replace('\r', '\n').strip('\n') + '\n'