# test_final_state.py

import os
import pytest

INI_PATH = "/home/user/services/payment_service.ini"
LOG_PATH = "/home/user/services/payment_database.log"

EXPECTED_INI_CONTENT = (
    "[general]\n"
    "service_name = PaymentService\n"
    "timeout = 30\n"
    "\n"
    "[database]\n"
    "host = db.production.internal\n"
    "port = 5432\n"
    "user = payments\n"
    "password = secret\n"
    "\n"
    "[logging]\n"
    "level = INFO\n"
)

EXPECTED_LOG_LINE = "db.production.internal:5432"

@pytest.mark.describe("Final state validation for payment_database.log creation and content")
def test_log_file_exists():
    """The log file must exist after task completion."""
    assert os.path.isfile(LOG_PATH), (
        f"Missing log file: {LOG_PATH}. "
        f"Ensure you create this file as required."
    )

@pytest.mark.describe("Final state validation for payment_database.log content")
def test_log_file_content():
    """The log file must contain exactly the expected host:port line, no extra whitespace or lines."""
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read the log file at {LOG_PATH}: {e}")

    # Check for extra whitespace, lines, etc.
    lines = content.splitlines()
    assert len(lines) == 1, (
        f"{LOG_PATH} should contain exactly one line, but found {len(lines)} lines.\n"
        f"Actual content:\n{content!r}"
    )
    line = lines[0]
    assert line == EXPECTED_LOG_LINE, (
        f"{LOG_PATH} contains incorrect content.\n"
        f"Expected: {EXPECTED_LOG_LINE!r}\n"
        f"Actual:   {line!r}\n"
        "Ensure you write only the host and port from the [database] section, separated by a colon, with no extra whitespace."
    )

@pytest.mark.describe("Final state validation for payment_service.ini immutability")
def test_ini_file_unchanged():
    """The INI file must remain unchanged after task completion."""
    assert os.path.isfile(INI_PATH), (
        f"The INI file {INI_PATH} is missing after task completion. It must not be deleted or moved."
    )
    try:
        with open(INI_PATH, "r", encoding="utf-8") as f:
            actual_content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read the INI file at {INI_PATH}: {e}")

    assert actual_content == EXPECTED_INI_CONTENT, (
        f"The content of {INI_PATH} has changed after task completion. "
        "Do not modify this file as part of your solution.\n"
        f"Expected content:\n{EXPECTED_INI_CONTENT!r}\n"
        f"Actual content:\n{actual_content!r}"
    )

@pytest.mark.describe("Final state validation for absence of extra lines/whitespace in log file")
def test_log_file_no_extra_whitespace():
    """The log file must not have preceding or trailing blank lines or spaces."""
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert all(line == line.rstrip('\r\n') + '\n' for line in lines), (
        f"{LOG_PATH} contains lines with trailing whitespace or non-unix line endings.\n"
        f"Actual lines: {lines!r}"
    )
    # The only line must be exactly the expected, plus a single newline
    assert lines[0].strip() == EXPECTED_LOG_LINE, (
        f"The only line in {LOG_PATH} is not exactly as expected.\n"
        f"Expected: {EXPECTED_LOG_LINE!r}\n"
        f"Actual:   {lines[0]!r}"
    )
    assert not lines[0].startswith(" ") and not lines[0].endswith(" \n"), (
        f"The log file line must not start or end with spaces.\n"
        f"Actual line: {lines[0]!r}"
    )