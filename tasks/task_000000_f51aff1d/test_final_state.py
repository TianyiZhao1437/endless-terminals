# test_final_state.py

import os
import stat
import pwd
import pytest
import subprocess
import re

LOG_FILE = "/home/user/logs/uptime.log"

@pytest.mark.order(1)
def test_uptime_log_exists_and_owned_by_user():
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE} does not exist after task completion. "
        "It must exist and be owned by 'user'."
    )
    st = os.stat(LOG_FILE)
    try:
        file_owner = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        file_owner = None
    assert file_owner == "user", (
        f"{LOG_FILE} is not owned by 'user' after task completion. "
        f"It is owned by '{file_owner}'. Set ownership to 'user'."
    )

@pytest.mark.order(2)
def test_uptime_log_permissions_are_secure():
    st = os.stat(LOG_FILE)
    expected_mode = stat.S_IRUSR | stat.S_IWUSR  # 0o600
    actual_mode = stat.S_IMODE(st.st_mode)
    assert actual_mode == expected_mode, (
        f"{LOG_FILE} permissions are {oct(actual_mode)}, expected 0o600 (-rw-------). "
        "Set permissions to 0600 so only the owner can read/write."
    )

@pytest.mark.order(3)
def test_uptime_log_appended_entry_format_and_content():
    with open(LOG_FILE, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) >= 3, (
        f"{LOG_FILE} should contain at least three lines (historical + new entry). "
        f"Found {len(lines)} lines. Ensure a new entry is appended."
    )

    # Check that the last line matches the required format
    last_line = lines[-1]
    line_re = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - uptime: .+$")
    assert line_re.match(last_line), (
        f"The last line of {LOG_FILE} is not in the required format:\n"
        f"YYYY-MM-DD HH:MM:SS - uptime: UPTIME_VALUE\n"
        f"Found: {last_line}"
    )

    # Check that the timestamp is valid and recent (within 5 minutes)
    import datetime
    timestamp_str = last_line.split(" - uptime: ")[0]
    try:
        log_time = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail(
            f"The timestamp '{timestamp_str}' in the last log entry is not in the "
            "required format YYYY-MM-DD HH:MM:SS."
        )

    now = datetime.datetime.now()
    delta = abs((now - log_time).total_seconds())
    assert delta < 300, (
        f"The timestamp in the last log entry ({timestamp_str}) is not recent. "
        f"Expected an entry appended within the last 5 minutes. "
        f"Current time is {now.strftime('%Y-%m-%d %H:%M:%S')}."
    )

    # Check that the uptime value matches the output of `uptime -p`
    try:
        uptime_output = subprocess.check_output(["uptime", "-p"], text=True).strip()
    except Exception as e:
        pytest.fail(
            f"Failed to get uptime value from 'uptime -p': {e}."
        )
    expected_suffix = f"uptime: {uptime_output}"
    assert last_line.endswith(expected_suffix), (
        f"The last log entry does not match the required uptime value.\n"
        f"Expected suffix: {expected_suffix}\n"
        f"Found: {last_line}"
    )