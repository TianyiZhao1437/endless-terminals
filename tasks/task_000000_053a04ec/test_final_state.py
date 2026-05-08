# test_final_state.py

import os
import pytest
import re
from datetime import datetime

LOGS_DIR = "/home/user/logs"
APP_LOG = os.path.join(LOGS_DIR, "app.log")
ERROR_LOG = os.path.join(LOGS_DIR, "error.log")

DEPLOYMENT_LINE_REGEX = re.compile(
    r"^Deployment completed: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC)$"
)

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_exists_after_deployment(filepath):
    assert os.path.isfile(filepath), (
        f"Log file '{filepath}' is missing after deployment: '{filepath}'."
        " Do not create new files or remove any log files."
    )

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_not_empty_after_deployment(filepath):
    try:
        with open(filepath, "r") as f:
            contents = f.read()
        assert contents.strip() != "", (
            f"Log file '{filepath}' is empty after deployment."
            " All original contents must be preserved and the deployment line appended."
        )
    except Exception as e:
        pytest.fail(f"Could not read '{filepath}': {e}")

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_ends_with_deployment_line(filepath):
    """
    Assert that the last line of the log file is the deployment completion line,
    in the exact UTC timestamp format.
    """
    try:
        with open(filepath, "r") as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Could not read '{filepath}': {e}")

    assert lines, (
        f"Log file '{filepath}' is empty after deployment."
        " All original contents must be preserved and the deployment line appended."
    )

    last_line = lines[-1]
    match = DEPLOYMENT_LINE_REGEX.match(last_line)
    assert match is not None, (
        f"The last line of '{filepath}' is:\n  {last_line!r}\n"
        "But it does not match the required deployment format:\n"
        "  Deployment completed: YYYY-MM-DD HH:MM:SS UTC\n"
        "Check your timestamp formatting and ensure the line is appended exactly."
    )

    # Validate the timestamp is a valid UTC datetime and is recent (within 10 minutes)
    timestamp_str = match.group(1)
    try:
        timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S UTC")
    except ValueError:
        pytest.fail(
            f"The deployment timestamp in '{filepath}' is malformed: {timestamp_str!r}.\n"
            "Expected format: YYYY-MM-DD HH:MM:SS UTC"
        )

    now_utc = datetime.utcnow()
    # Allow up to 10 minutes tolerance for execution time
    delta_seconds = abs((now_utc - timestamp_dt).total_seconds())
    assert delta_seconds < 600, (
        f"Deployment timestamp in '{filepath}' is not recent:\n"
        f"  Found: {timestamp_str}\n"
        f"  Current UTC: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        "Timestamp must be generated at deployment time in UTC format."
    )

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_only_appended(filepath):
    """
    Assert that only a single line was appended to the log file,
    i.e. all previous contents are preserved, and only the deployment line is added.
    """
    try:
        with open(filepath, "r") as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Could not read '{filepath}': {e}")

    assert len(lines) >= 2, (
        f"Log file '{filepath}' must contain original contents and the deployment line."
        " It appears too short after deployment."
    )
    # The deployment line must only appear as the very last line
    deployment_line_count = sum(
        1 for line in lines if DEPLOYMENT_LINE_REGEX.match(line)
    )
    assert deployment_line_count == 1, (
        f"Deployment line found {deployment_line_count} times in '{filepath}'.\n"
        "You must only append the deployment line once, as the very last line."
    )
    assert DEPLOYMENT_LINE_REGEX.match(lines[-1]), (
        f"The deployment line is not at the end of '{filepath}'.\n"
        "It must be appended as the very last line, after all previous contents."
    )