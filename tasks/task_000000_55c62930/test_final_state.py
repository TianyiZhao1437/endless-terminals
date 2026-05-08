# test_final_state.py

import os
import pytest
import stat
import subprocess

HOME_DIR = "/home/user"
DISK_USAGE_LOG = "/home/user/disk_usage.log"

def get_expected_disk_usage_line():
    """
    Get the expected disk usage line by running 'du -sh /home/user'.
    Returns the string: 'Total disk usage of /home/user: [SIZE]'
    """
    try:
        # Run 'du -sh /home/user' and capture output
        result = subprocess.run(
            ["du", "-sh", HOME_DIR],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
    except FileNotFoundError:
        pytest.skip("'du' command not found on this system. Cannot determine expected disk usage.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run 'du -sh {HOME_DIR}': {e.stderr.strip()}")

    line = result.stdout.strip()
    if not line:
        pytest.fail(f"'du -sh {HOME_DIR}' produced no output.")

    # The output is like: "4.0K   /home/user"
    parts = line.split()
    if len(parts) < 2:
        pytest.fail(f"Unexpected output from 'du -sh {HOME_DIR}': '{line}'")
    size = parts[0]
    return f"Total disk usage of /home/user: {size}"

@pytest.mark.order(1)
def test_disk_usage_log_exists():
    """Check that /home/user/disk_usage.log exists after the task."""
    assert os.path.isfile(DISK_USAGE_LOG), (
        f"Missing file: {DISK_USAGE_LOG}. "
        "The disk usage log file must exist after the task is completed."
    )

@pytest.mark.order(2)
def test_disk_usage_log_content():
    """
    Check that /home/user/disk_usage.log contains exactly one line,
    formatted as 'Total disk usage of /home/user: [SIZE]', with no extra whitespace or lines.
    """
    assert os.path.isfile(DISK_USAGE_LOG), (
        f"File not found: {DISK_USAGE_LOG}. Cannot check content."
    )
    with open(DISK_USAGE_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove trailing newline characters
    lines_stripped = [line.rstrip('\n') for line in lines]

    assert len(lines_stripped) == 1, (
        f"{DISK_USAGE_LOG} should contain exactly one line. "
        f"Found {len(lines_stripped)} lines."
    )

    log_line = lines_stripped[0]
    expected_line = get_expected_disk_usage_line()

    # Check for exact match
    assert log_line == expected_line, (
        f"Incorrect content in {DISK_USAGE_LOG}.\n"
        f"Expected: '{expected_line}'\n"
        f"Found:    '{log_line}'"
    )

    # Check for trailing spaces
    assert log_line == log_line.rstrip(), (
        f"{DISK_USAGE_LOG} contains trailing spaces on the line."
    )

@pytest.mark.order(3)
def test_disk_usage_log_permissions():
    """
    Check that /home/user/disk_usage.log is readable and writable by the user.
    """
    assert os.path.isfile(DISK_USAGE_LOG), (
        f"File not found: {DISK_USAGE_LOG}. Cannot check permissions."
    )
    st = os.stat(DISK_USAGE_LOG)
    user_read = bool(st.st_mode & stat.S_IRUSR)
    user_write = bool(st.st_mode & stat.S_IWUSR)

    assert user_read, (
        f"{DISK_USAGE_LOG} is not readable by the user."
    )
    assert user_write, (
        f"{DISK_USAGE_LOG} is not writable by the user."
    )

@pytest.mark.order(4)
def test_no_extra_files_created():
    """
    Check that no extra files were created in /home/user besides disk_usage.log.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Missing directory: {HOME_DIR}. Cannot check for extra files."
    )
    files = [os.path.join(HOME_DIR, f) for f in os.listdir(HOME_DIR)]
    log_files = [f for f in files if f == DISK_USAGE_LOG]
    extra_files = [f for f in files if f != DISK_USAGE_LOG and os.path.isfile(f)]

    assert log_files, (
        f"{DISK_USAGE_LOG} not found in {HOME_DIR}."
    )
    assert not extra_files, (
        f"Extra files found in {HOME_DIR} after the task was completed: {extra_files}. "
        "No files other than disk_usage.log should have been created."
    )