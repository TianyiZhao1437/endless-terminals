# test_initial_state.py

import os
import pytest

INI_PATH = "/home/user/services/payment_service.ini"
LOG_PATH = "/home/user/services/payment_database.log"

@pytest.mark.describe("Initial state validation for payment_service.ini extraction task")
def test_payment_service_ini_exists():
    """The INI file must exist at the specified path before the student performs the action."""
    assert os.path.isfile(INI_PATH), (
        f"Missing required INI file: {INI_PATH}. "
        f"Ensure the file exists at this path before starting."
    )

@pytest.mark.describe("Initial state validation for payment_database.log absence")
def test_payment_database_log_does_not_exist():
    """The log file should NOT exist before the student performs the action."""
    assert not os.path.exists(LOG_PATH), (
        f"The log file {LOG_PATH} should NOT exist before you run your solution."
    )

@pytest.mark.describe("Initial state validation for directory structure")
def test_services_directory_exists():
    """The /home/user/services directory must exist."""
    services_dir = os.path.dirname(INI_PATH)
    assert os.path.isdir(services_dir), (
        f"Missing directory: {services_dir}. "
        "Ensure the directory exists before starting."
    )

@pytest.mark.describe("Initial state validation for payment_service.ini content")
def test_ini_content_correct():
    """The INI file must contain the expected content for the test to be valid."""
    expected_content = (
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
    try:
        with open(INI_PATH, "r", encoding="utf-8") as f:
            actual_content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read the INI file at {INI_PATH}: {e}")

    assert actual_content == expected_content, (
        f"The content of {INI_PATH} does not match the expected initial state.\n"
        "Expected content:\n"
        f"{expected_content!r}\n"
        "Actual content:\n"
        f"{actual_content!r}\n"
        "Please restore the file to the expected state before starting."
    )