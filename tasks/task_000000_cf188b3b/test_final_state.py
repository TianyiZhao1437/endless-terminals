# test_final_state.py

import os
import pytest
import pwd
import stat

HOME = '/home/user'
API_CODE_DIR = os.path.join(HOME, 'old_api_code')
TEST_SCRIPT = os.path.join(API_CODE_DIR, 'test_api.py')
OUTPUT_LOG = os.path.join(HOME, 'api_test_output.log')

EXPECTED_OUTPUT = "API test successful. All endpoints returned 200 OK.\n"


def test_output_log_exists():
    assert os.path.isfile(OUTPUT_LOG), (
        f"The output log '{OUTPUT_LOG}' does not exist.\n"
        "You must save the script's console output verbatim to this file after running test_api.py."
    )


def test_output_log_contents():
    try:
        with open(OUTPUT_LOG, 'r', encoding='utf-8') as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(f"Could not open '{OUTPUT_LOG}': {e}")

    # The output must be exactly as displayed in the terminal, including newline
    assert contents == EXPECTED_OUTPUT, (
        f"The contents of '{OUTPUT_LOG}' do not match the expected output.\n"
        "Expected output (including newline):\n"
        f"{EXPECTED_OUTPUT!r}\n"
        "Found:\n"
        f"{contents!r}\n"
        "Ensure you captured the output exactly as it appeared in the terminal, with no extra or missing lines."
    )


def test_output_log_ownership_and_permissions():
    stat_info = os.stat(OUTPUT_LOG)
    file_uid = stat_info.st_uid
    file_mode = stat_info.st_mode

    try:
        user_info = pwd.getpwnam('user')
    except KeyError:
        pytest.skip("User 'user' does not exist on this system; skipping ownership test.")

    assert file_uid == user_info.pw_uid, (
        f"'{OUTPUT_LOG}' is not owned by the 'user' account (uid {user_info.pw_uid}).\n"
        f"Current owner UID is {file_uid}."
    )

    # Check that user has read permission
    user_read = bool(file_mode & stat.S_IRUSR)
    assert user_read, (
        f"The file '{OUTPUT_LOG}' is not readable by the user.\n"
        "Please ensure the file permissions allow the user to read the log."
    )

def test_output_log_is_not_empty():
    size = os.path.getsize(OUTPUT_LOG)
    assert size > 0, (
        f"The file '{OUTPUT_LOG}' is empty.\n"
        "It should contain the output from running the test_api.py script."
    )