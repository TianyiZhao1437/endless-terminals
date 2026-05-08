# test_final_state.py

import os
import pytest
import stat

MONITORING_DIR = "/home/user/monitoring_logs"
APP_LOG = "/home/user/monitoring_logs/app.log"
ALERTS_SUMMARY = "/home/user/monitoring_logs/alerts_summary.txt"

EXPECTED_ALERTS_SUMMARY_CONTENT = (
    "ALERT SUMMARY — Events matching 'CRITICAL' or 'ERROR'\n"
    "2024-06-15 08:23:41 CRITICAL Database connection lost\n"
    "2024-06-15 08:24:00 ERROR Failed to load configuration file\n"
)

EXPECTED_ALERT_LINES = [
    "2024-06-15 08:23:41 CRITICAL Database connection lost",
    "2024-06-15 08:24:00 ERROR Failed to load configuration file",
]

HEADER_LINE = "ALERT SUMMARY — Events matching 'CRITICAL' or 'ERROR'"


def test_alerts_summary_exists():
    assert os.path.isfile(ALERTS_SUMMARY), (
        f"{ALERTS_SUMMARY} does not exist. "
        "You must create this file with the correct alert summary after processing the log."
    )


def test_alerts_summary_contents_exact():
    try:
        with open(ALERTS_SUMMARY, "r", encoding="utf-8") as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {ALERTS_SUMMARY}: {e}")

    assert contents == EXPECTED_ALERTS_SUMMARY_CONTENT, (
        f"{ALERTS_SUMMARY} content is incorrect.\n"
        f"--- Expected ---\n{EXPECTED_ALERTS_SUMMARY_CONTENT!r}\n"
        f"--- Found ---\n{contents!r}\n"
        "Check for extra/missing/blank lines, header correctness, or incorrect log lines."
    )


def test_alerts_summary_no_blank_lines_between_header_and_events():
    with open(ALERTS_SUMMARY, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    assert lines, f"{ALERTS_SUMMARY} is empty."
    assert lines[0] == HEADER_LINE, (
        f"First line of {ALERTS_SUMMARY} is incorrect. "
        f"Expected header:\n{HEADER_LINE!r}\nFound:\n{lines[0]!r}"
    )
    # There must be no blank lines after the header and before the events
    if len(lines) > 1:
        assert lines[1] != '', (
            f"Blank line found after header in {ALERTS_SUMMARY}. "
            "There should be no blank lines between header and event lines."
        )


def test_alerts_summary_only_matching_lines_and_order():
    with open(ALERTS_SUMMARY, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Ignore header
    event_lines = lines[1:]
    assert event_lines == EXPECTED_ALERT_LINES, (
        f"Event lines in {ALERTS_SUMMARY} do not match expected lines or order.\n"
        f"--- Expected ---\n{EXPECTED_ALERT_LINES!r}\n"
        f"--- Found ---\n{event_lines!r}\n"
        "Ensure only lines containing 'CRITICAL' or 'ERROR' are included, in order, with no extras."
    )


def test_alerts_summary_no_extra_lines_or_spaces():
    with open(ALERTS_SUMMARY, "r", encoding="utf-8") as f:
        raw = f.read()

    # Check for trailing newlines or spaces at the end
    assert not raw.endswith("\n\n"), (
        f"{ALERTS_SUMMARY} has extra blank lines at the end."
    )
    # Check for trailing/leading whitespace on lines
    for lineno, line in enumerate(raw.splitlines(), 1):
        assert line == line.strip(), (
            f"Line {lineno} in {ALERTS_SUMMARY} has leading/trailing whitespace: {line!r}"
        )


def test_alerts_summary_permissions():
    st = os.stat(ALERTS_SUMMARY)
    # Ensure user has read and write permissions
    user_perms = stat.S_IMODE(st.st_mode) & 0o600
    assert user_perms == 0o600 or user_perms == 0o644 or user_perms == 0o660 or user_perms == 0o666, (
        f"{ALERTS_SUMMARY} permissions are too restrictive or too open. "
        "File must be readable and writable by the user (e.g., 600, 644, 660, or 666). "
        f"Current permissions: {oct(stat.S_IMODE(st.st_mode))}"
    )