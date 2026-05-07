# test_initial_state.py

import os
import pytest

SECURITY_NOTES_PATH = "/home/user/security_notes.txt"
SECURITY_NOTES_REDACTED_PATH = "/home/user/security_notes_redacted.txt"
REDACTION_LOG_PATH = "/home/user/redaction_log.txt"

EXPECTED_SECURITY_NOTES = [
    "Welcome to the security notes file.",
    "Password: mysecret123",
    "Please update by Friday.",
    "User password: qwerty",
    "End of document."
]

@pytest.mark.describe("Initial OS/filesystem state before task")
def test_security_notes_txt_exists_and_content():
    """Check that /home/user/security_notes.txt exists and contains the correct content before the task."""
    assert os.path.isfile(SECURITY_NOTES_PATH), (
        f"Missing file: {SECURITY_NOTES_PATH}. "
        "This file must exist before starting the task."
    )
    with open(SECURITY_NOTES_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    assert lines == EXPECTED_SECURITY_NOTES, (
        f"The contents of {SECURITY_NOTES_PATH} are incorrect.\n"
        "Expected:\n" +
        "\n".join(EXPECTED_SECURITY_NOTES) +
        "\nActual:\n" +
        "\n".join(lines)
    )

def test_security_notes_redacted_txt_does_not_exist():
    """Check that /home/user/security_notes_redacted.txt does NOT exist before the task."""
    assert not os.path.exists(SECURITY_NOTES_REDACTED_PATH), (
        f"{SECURITY_NOTES_REDACTED_PATH} should NOT exist before the task starts."
    )

def test_redaction_log_txt_does_not_exist():
    """Check that /home/user/redaction_log.txt does NOT exist before the task."""
    assert not os.path.exists(REDACTION_LOG_PATH), (
        f"{REDACTION_LOG_PATH} should NOT exist before the task starts."
    )