# test_final_state.py

import os
import stat
import re
import pytest

SCRAPE_LOG_PATH = "/home/user/scrape_audit.log"
EXPECTED_H1 = "Herman Melville - Moby-Dick"

ISO8601_UTC_REGEX = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
)

def read_log_file():
    try:
        with open(SCRAPE_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return lines
    except Exception as e:
        pytest.fail(f"Failed to read {SCRAPE_LOG_PATH}: {e}")

def test_scrape_audit_log_exists():
    """
    The file /home/user/scrape_audit.log must exist after task completion.
    """
    assert os.path.exists(SCRAPE_LOG_PATH), (
        f"{SCRAPE_LOG_PATH} does not exist. "
        f"Did you create the log file in the correct location?"
    )
    assert os.path.isfile(SCRAPE_LOG_PATH), (
        f"{SCRAPE_LOG_PATH} exists but is not a regular file."
    )

def test_scrape_audit_log_permissions():
    """
    The log file should be readable and writable by the user.
    """
    st = os.stat(SCRAPE_LOG_PATH)
    # Owner read/write
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"{SCRAPE_LOG_PATH} is not readable by the user."
    )
    assert bool(st.st_mode & stat.S_IWUSR), (
        f"{SCRAPE_LOG_PATH} is not writable by the user."
    )

def test_scrape_audit_log_content():
    """
    The log file must contain exactly one line in the correct format:
    Timestamp: <ISO-8601 datetime> | H1: Herman Melville - Moby-Dick
    """
    lines = read_log_file()
    assert len(lines) == 1, (
        f"{SCRAPE_LOG_PATH} should contain exactly 1 line, "
        f"but contains {len(lines)} lines."
    )

    line = lines[0].rstrip('\n')
    # Check for exact format: Timestamp: <ISO-8601 datetime> | H1: <heading text>
    pat = re.compile(
        r"^Timestamp: (?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) \| H1: (?P<h1>.+)$"
    )
    m = pat.match(line)
    assert m is not None, (
        f"Line in {SCRAPE_LOG_PATH} is not in the required format.\n"
        f"Expected: Timestamp: <ISO-8601 datetime> | H1: {EXPECTED_H1}\n"
        f"Found:    {line}"
    )
    # Validate the timestamp is a valid ISO8601 UTC time
    ts = m.group("ts")
    assert ISO8601_UTC_REGEX.fullmatch(ts), (
        f"Timestamp in log file is not a valid ISO-8601 UTC datetime: '{ts}'"
    )

    # Validate the H1 content is exactly as expected (no extra whitespace!)
    h1 = m.group("h1")
    assert h1 == EXPECTED_H1, (
        f"H1 text in log file is incorrect.\n"
        f"Expected: '{EXPECTED_H1}'\n"
        f"Found:    '{h1}'"
    )

def test_scrape_audit_log_no_extra_content():
    """
    There should be no extra blank lines or trailing content in the log file.
    """
    with open(SCRAPE_LOG_PATH, "rb") as f:
        content = f.read()
    # Should be exactly one line ending with '\n' or not, but no extra data
    num_newlines = content.count(b'\n')
    assert num_newlines <= 1, (
        f"{SCRAPE_LOG_PATH} should contain only one line (with one optional newline at the end), "
        f"but found {num_newlines} newline characters. "
        f"Check for extra blank lines or trailing whitespace."
    )
    # No trailing whitespace or extra blank lines
    text = content.decode('utf-8')
    assert not text.endswith('\n\n'), (
        f"{SCRAPE_LOG_PATH} has extra blank lines at the end."
    )