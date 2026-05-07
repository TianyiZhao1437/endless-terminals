"""
test_final_state.py

Pytest suite to validate the FINAL state after redacting sensitive lines from
"/home/user/security_notes.txt", saving the updated content to
"/home/user/security_notes_redacted.txt", and logging replaced lines to
"/home/user/redaction_log.txt".

Rules:
- Only Python stdlib and pytest are used.
- Absolute paths are checked.
- Failures explain exactly what is wrong.
"""

import os
import pytest

SECURITY_NOTES_PATH = "/home/user/security_notes.txt"
SECURITY_NOTES_REDACTED_PATH = "/home/user/security_notes_redacted.txt"
REDACTION_LOG_PATH = "/home/user/redaction_log.txt"

# Truth values for final state

EXPECTED_SECURITY_NOTES_TXT = [
    "Welcome to the security notes file.",
    "Password: mysecret123",
    "Please update by Friday.",
    "User password: qwerty",
    "End of document."
]

EXPECTED_SECURITY_NOTES_REDACTED_TXT = [
    "Welcome to the security notes file.",
    "***REMOVED IN DOCUMENT REVIEW***",
    "Please update by Friday.",
    "***REMOVED IN DOCUMENT REVIEW***",
    "End of document."
]

EXPECTED_REDACTION_LOG_TXT = [
    'Original line: "Password: mysecret123"',
    'Original line: "User password: qwerty"'
]


@pytest.mark.describe("Final OS/filesystem state after task completion")
def test_security_notes_txt_unchanged():
    """
    Verify that /home/user/security_notes.txt still exists and is unchanged.
    """
    assert os.path.isfile(SECURITY_NOTES_PATH), (
        f"Missing file: {SECURITY_NOTES_PATH}. "
        "This file must remain unchanged after the task."
    )
    with open(SECURITY_NOTES_PATH, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f.readlines()]
    assert actual_lines == EXPECTED_SECURITY_NOTES_TXT, (
        f"The contents of {SECURITY_NOTES_PATH} have changed.\n"
        "Expected:\n" +
        "\n".join(EXPECTED_SECURITY_NOTES_TXT) +
        "\nActual:\n" +
        "\n".join(actual_lines)
    )


def test_security_notes_redacted_txt_exists_and_content():
    """
    Verify that /home/user/security_notes_redacted.txt exists and is correctly redacted.
    """
    assert os.path.isfile(SECURITY_NOTES_REDACTED_PATH), (
        f"Missing file: {SECURITY_NOTES_REDACTED_PATH}. "
        "This file must exist after the task is completed."
    )
    with open(SECURITY_NOTES_REDACTED_PATH, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f.readlines()]
    assert actual_lines == EXPECTED_SECURITY_NOTES_REDACTED_TXT, (
        f"The contents of {SECURITY_NOTES_REDACTED_PATH} are incorrect.\n"
        "Expected:\n" +
        "\n".join(EXPECTED_SECURITY_NOTES_REDACTED_TXT) +
        "\nActual:\n" +
        "\n".join(actual_lines) +
        "\n\n"
        "Check that only lines containing 'password' (case-insensitive) are replaced with "
        "'***REMOVED IN DOCUMENT REVIEW***', and the formatting is preserved."
    )


def test_redaction_log_txt_exists_and_content():
    """
    Verify that /home/user/redaction_log.txt exists and contains the correct log entries,
    in the correct order and format.
    """
    assert os.path.isfile(REDACTION_LOG_PATH), (
        f"Missing file: {REDACTION_LOG_PATH}. "
        "This file must exist after the task is completed."
    )
    with open(REDACTION_LOG_PATH, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f.readlines()]
    assert actual_lines == EXPECTED_REDACTION_LOG_TXT, (
        f"The contents of {REDACTION_LOG_PATH} are incorrect.\n"
        "Expected:\n" +
        "\n".join(EXPECTED_REDACTION_LOG_TXT) +
        "\nActual:\n" +
        "\n".join(actual_lines) +
        "\n\n"
        "Check that each replaced line from security_notes.txt is logged in order "
        "as: Original line: \"<line content>\""
    )