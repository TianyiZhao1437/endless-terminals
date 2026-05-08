# test_final_state.py

import os
import pytest

HOME = '/home/user'
MEMORY_LOG_PATH = os.path.join(HOME, 'memory_check.log')

# The "truth" content expected in the log file, with exact formatting.
EXPECTED_MEMORY_LOG = (
    "              total        used        free      shared  buff/cache   available\n"
    "Mem:           7987        2509        3811          80        1666        5229\n"
    "Swap:          2047           0        2047\n"
)

def test_memory_check_log_exists():
    """
    The output file /home/user/memory_check.log MUST exist after the student performs the action.
    """
    assert os.path.exists(MEMORY_LOG_PATH), (
        f"The file {MEMORY_LOG_PATH} does not exist. "
        "You must create the log file at the specified absolute path."
    )

def test_memory_check_log_is_file():
    """
    The output file /home/user/memory_check.log MUST be a regular file (not a directory or symlink).
    """
    assert os.path.isfile(MEMORY_LOG_PATH), (
        f"{MEMORY_LOG_PATH} exists but is not a regular file."
    )

def test_memory_check_log_content_exact():
    """
    The log file MUST contain only the required memory and swap statistics,
    formatted EXACTLY as specified (including column headers, alignment, integer values, and no extra lines).
    """
    with open(MEMORY_LOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip trailing whitespace for comparison, but preserve leading whitespace and newlines
    # (since alignment matters).
    content_stripped = content.rstrip('\r\n')
    expected_stripped = EXPECTED_MEMORY_LOG.rstrip('\r\n')

    assert content_stripped == expected_stripped, (
        f"The contents of {MEMORY_LOG_PATH} do not match the required format or values.\n"
        f"\n"
        f"Expected content:\n"
        f"---\n{EXPECTED_MEMORY_LOG}---\n"
        f"Actual content:\n"
        f"---\n{content}---\n"
        f"\n"
        f"Check that:\n"
        f"- Only the header and two rows (Mem: and Swap:) are present\n"
        f"- All column alignments and spacing are exact\n"
        f"- No extra lines, headers, or summary text appear\n"
        f"- All integer values match the required output\n"
    )

def test_memory_check_log_no_extra_lines():
    """
    Ensure the log file contains ONLY three lines: header, Mem:, Swap:.
    """
    with open(MEMORY_LOG_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 3, (
        f"{MEMORY_LOG_PATH} should contain exactly three lines (header, Mem:, Swap:), "
        f"but found {len(lines)} lines.\n"
        f"Actual lines:\n{''.join(lines)}"
    )

def test_no_unexpected_files_created():
    """
    No other files or directories should be created as part of the task.
    Only /home/user/memory_check.log is allowed.
    """
    allowed_files = {MEMORY_LOG_PATH}
    user_home_contents = {os.path.join(HOME, fname) for fname in os.listdir(HOME)}
    unexpected = user_home_contents - allowed_files
    assert not unexpected, (
        f"Unexpected files or directories found in {HOME}: {unexpected}.\n"
        f"Only {MEMORY_LOG_PATH} should exist after completing the task."
    )