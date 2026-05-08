# test_final_state.py

import os
import stat
import pwd
import pytest

PIPELINE_UTIL_DIR = "/home/user/pipeline_util"
NUMBERS_TXT = os.path.join(PIPELINE_UTIL_DIR, "numbers.txt")
PROCESS_SH = os.path.join(PIPELINE_UTIL_DIR, "process_numbers.sh")
PIPELINE_LOG = os.path.join(PIPELINE_UTIL_DIR, "pipeline_test.log")
USER = "user"


def test_pipeline_util_directory_exists():
    assert os.path.isdir(PIPELINE_UTIL_DIR), (
        f"Required directory does not exist: {PIPELINE_UTIL_DIR}"
    )


def test_numbers_txt_exists_and_contents():
    assert os.path.isfile(NUMBERS_TXT), (
        f"Required file does not exist: {NUMBERS_TXT}"
    )
    with open(NUMBERS_TXT, "r") as f:
        contents = f.read()
    expected = "3\n7\nnotanumber\n9\n"
    assert contents == expected, (
        f"File {NUMBERS_TXT} does not have the expected contents.\n"
        f"Expected:\n{repr(expected)}\nGot:\n{repr(contents)}"
    )


def test_process_numbers_sh_exists_and_permissions():
    assert os.path.isfile(PROCESS_SH), (
        f"Required script does not exist: {PROCESS_SH}"
    )

    st = os.stat(PROCESS_SH)
    expected_mode = 0o755
    actual_mode = stat.S_IMODE(st.st_mode)
    assert actual_mode == expected_mode, (
        f"Script {PROCESS_SH} does not have mode 0755 (executable).\n"
        f"Actual mode: {oct(actual_mode)}"
    )

    owner_uid = st.st_uid
    owner_name = pwd.getpwuid(owner_uid).pw_name
    assert owner_name == USER, (
        f"Script {PROCESS_SH} is not owned by '{USER}'.\n"
        f"Actual owner: {owner_name}"
    )


def test_process_numbers_sh_contents_implements_spec():
    with open(PROCESS_SH, "r") as f:
        script = f.read()

    # Check for shebang line
    assert script.startswith("#!"), (
        f"Script {PROCESS_SH} does not start with a shebang (#!)."
    )

    # Check for reference to numbers.txt at correct absolute path
    assert NUMBERS_TXT in script, (
        f"Script {PROCESS_SH} does not reference the required numbers.txt file at path {NUMBERS_TXT}."
    )

    # Check for error messages in script
    assert "numbers.txt not found" in script, (
        f"Script {PROCESS_SH} does not implement the required error message for missing numbers.txt."
    )
    assert "invalid data on line" in script, (
        f"Script {PROCESS_SH} does not implement the required error message for invalid data."
    )

    # Check that script uses line numbers (i.e., outputs X for line)
    assert "invalid data on line" in script, (
        f"Script {PROCESS_SH} must output the line number for the first offending line."
    )

    # Check that script sums integers and outputs result (look for arithmetic or sum logic)
    # Acceptable: awk, bash arithmetic, etc.
    sum_logic_found = (
        ("awk" in script and "sum" in script)
        or ("expr" in script)
        or ("let" in script)
        or ("((sum" in script)
        or ("bc" in script)
        or ("total" in script)
    )
    assert sum_logic_found, (
        f"Script {PROCESS_SH} does not appear to implement summing of integers from numbers.txt."
    )


def test_pipeline_test_log_exists_and_correct_output():
    assert os.path.isfile(PIPELINE_LOG), (
        f"Required log file does not exist: {PIPELINE_LOG}"
    )
    with open(PIPELINE_LOG, "r") as f:
        log_contents = f.read()
    expected = "ERROR: invalid data on line 3\n"
    assert log_contents == expected, (
        f"Log file {PIPELINE_LOG} does not have the expected output.\n"
        f"Expected:\n{repr(expected)}\nGot:\n{repr(log_contents)}"
    )


def test_numbers_txt_unchanged():
    # Repeated to ensure file is not modified during the task
    with open(NUMBERS_TXT, "r") as f:
        contents = f.read()
    expected = "3\n7\nnotanumber\n9\n"
    assert contents == expected, (
        f"File {NUMBERS_TXT} has been modified during the task.\n"
        f"Expected:\n{repr(expected)}\nGot:\n{repr(contents)}"
    )