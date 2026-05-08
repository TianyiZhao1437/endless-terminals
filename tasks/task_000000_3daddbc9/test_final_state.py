# test_final_state.py

import os
import stat
import pytest

ALERTS_DIR = '/home/user/alerts'
RULES_CONF = os.path.join(ALERTS_DIR, 'rules.conf')
PATCH_FILE = os.path.join(ALERTS_DIR, 'rules.conf.patch')
PATCH_OUTPUT_LOG = os.path.join(ALERTS_DIR, 'patch_output.log')

# The expected content of /home/user/alerts/rules.conf after patch applied
RULES_CONF_FINAL_CONTENT = """[alert1]
name: High Memory Usage
threshold: 90
enabled: true

[alert2]
name: High CPU Load
threshold: 85
enabled: true
"""

# The expected content of /home/user/alerts/patch_output.log
PATCH_OUTPUT_LOG_CONTENT = "patching file rules.conf\n"

@pytest.mark.order(1)
def test_alerts_directory_still_exists():
    assert os.path.isdir(ALERTS_DIR), (
        f"Directory '{ALERTS_DIR}' is missing after patch application. "
        "It must remain present."
    )

@pytest.mark.order(2)
def test_alerts_directory_writable():
    st = os.stat(ALERTS_DIR)
    mode = st.st_mode
    assert mode & stat.S_IWUSR, (
        f"Directory '{ALERTS_DIR}' is not writable by the user after patch application. "
        "Permissions must remain correct."
    )

@pytest.mark.order(3)
def test_rules_conf_exists():
    assert os.path.isfile(RULES_CONF), (
        f"File '{RULES_CONF}' is missing after patch application. "
        "It must still exist and be updated."
    )

@pytest.mark.order(4)
def test_rules_conf_content_final():
    with open(RULES_CONF, 'r', encoding='utf-8') as f:
        actual = f.read()
    expected = RULES_CONF_FINAL_CONTENT
    # Normalize line endings for robust comparison
    actual_normalized = _normalize_content(actual)
    expected_normalized = _normalize_content(expected)
    assert actual_normalized == expected_normalized, (
        f"File '{RULES_CONF}' does not contain the expected patched content.\n"
        "Expected:\n"
        f"{expected}"
        "\nActual:\n"
        f"{actual}"
    )

@pytest.mark.order(5)
def test_patch_file_still_exists():
    assert os.path.isfile(PATCH_FILE), (
        f"Patch file '{PATCH_FILE}' is missing after patch application. "
        "It should not be removed or altered."
    )

@pytest.mark.order(6)
def test_patch_output_log_exists():
    assert os.path.isfile(PATCH_OUTPUT_LOG), (
        f"Patch output log '{PATCH_OUTPUT_LOG}' is missing. "
        "You must create this file capturing the patch command's output."
    )

@pytest.mark.order(7)
def test_patch_output_log_content():
    with open(PATCH_OUTPUT_LOG, 'r', encoding='utf-8') as f:
        actual = f.read()
    expected = PATCH_OUTPUT_LOG_CONTENT
    # Normalize line endings for robust comparison
    actual_normalized = _normalize_content(actual)
    expected_normalized = _normalize_content(expected)
    assert actual_normalized == expected_normalized, (
        f"File '{PATCH_OUTPUT_LOG}' does not contain exactly the expected patch command output.\n"
        "It must contain ONLY the output from running the patch command, with no extra lines or text.\n"
        "Expected:\n"
        f"{expected}"
        "\nActual:\n"
        f"{actual}"
    )

@pytest.mark.order(8)
def test_patch_output_log_permissions():
    st = os.stat(PATCH_OUTPUT_LOG)
    mode = st.st_mode
    assert mode & stat.S_IRUSR, (
        f"File '{PATCH_OUTPUT_LOG}' is not readable by the user."
    )
    assert mode & stat.S_IWUSR, (
        f"File '{PATCH_OUTPUT_LOG}' is not writable by the user."
    )

def _normalize_content(s):
    # Normalize line endings and strip trailing whitespace/newlines for fair comparison
    return s.replace('\r\n', '\n').replace('\r', '\n').strip('\n') + '\n'