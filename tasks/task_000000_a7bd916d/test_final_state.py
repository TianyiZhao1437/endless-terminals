# test_final_state.py

import os
import stat
import pytest

BACKUP_DIR = "/home/user/backup_restore_test"
RESTORE_DIR = os.path.join(BACKUP_DIR, "restore_dir")
LOG_FILE = os.path.join(BACKUP_DIR, "restore_verification.log")

EXPECTED_TOP_LEVEL = {
    ".git": "dir",
    "README.md": "file",
    "main.py": "file",
}

EXPECTED_LOG_LINES = [
    ".git",
    "README.md",
    "main.py",
]

def test_restore_dir_exists_and_has_expected_contents():
    assert os.path.isdir(RESTORE_DIR), (
        f"Restore directory '{RESTORE_DIR}' does not exist. "
        f"Ensure you extracted the backup archive to this location."
    )
    entries = os.listdir(RESTORE_DIR)
    entries_set = set(entries)
    expected_set = set(EXPECTED_TOP_LEVEL.keys())

    missing = expected_set - entries_set
    extra = entries_set - expected_set

    assert not missing, (
        f"Restore directory '{RESTORE_DIR}' is missing required items: {', '.join(sorted(missing))}."
    )
    assert not extra, (
        f"Restore directory '{RESTORE_DIR}' contains unexpected items: {', '.join(sorted(extra))}."
    )

    for name, kind in EXPECTED_TOP_LEVEL.items():
        path = os.path.join(RESTORE_DIR, name)
        if kind == "dir":
            assert os.path.isdir(path), (
                f"Expected '{name}' to be a directory inside '{RESTORE_DIR}', but it is missing or not a directory."
            )
        elif kind == "file":
            assert os.path.isfile(path), (
                f"Expected '{name}' to be a file inside '{RESTORE_DIR}', but it is missing or not a file."
            )
        else:
            pytest.fail(f"Internal error: unknown expected kind '{kind}' for '{name}'.")

def test_log_file_exists_and_is_readable():
    assert os.path.isfile(LOG_FILE), (
        f"Restore verification log '{LOG_FILE}' does not exist. "
        "Ensure you created the log file after restoring."
    )
    # Check that the file is readable
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(
            f"Could not read log file '{LOG_FILE}': {e}"
        )

def test_log_file_contents_are_correct():
    # Check contents exactly match expected lines
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Could not read log file '{LOG_FILE}': {e}")

    # Strip trailing newlines
    lines = [line.rstrip("\r\n") for line in lines]

    if lines != EXPECTED_LOG_LINES:
        # Find detailed differences
        expected_set = set(EXPECTED_LOG_LINES)
        lines_set = set(lines)

        missing = expected_set - lines_set
        extra = lines_set - expected_set
        wrong_order = lines != sorted(lines)

        msg = [f"Log file '{LOG_FILE}' does not match the required format or contents."]
        if missing:
            msg.append(f"  Missing entries: {', '.join(sorted(missing))}.")
        if extra:
            msg.append(f"  Unexpected entries: {', '.join(sorted(extra))}.")
        if lines != EXPECTED_LOG_LINES:
            msg.append(
                f"  Expected lines (in order):\n    " +
                "\n    ".join(EXPECTED_LOG_LINES) +
                "\n  Found lines (in order):\n    " +
                "\n    ".join(lines)
            )
        pytest.fail("\n".join(msg))

def test_log_file_has_no_extra_blank_lines_or_whitespace():
    with open(LOG_FILE, "r") as f:
        raw = f.read()
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        assert line == line.strip(), (
            f"Line {i+1} in '{LOG_FILE}' has unexpected leading/trailing whitespace: {repr(line)}"
        )
    assert all(line for line in lines), (
        f"Log file '{LOG_FILE}' has blank lines, which are not allowed."
    )
    # Check for trailing newline at end of file (optional, but must not have extra blank lines)
    if raw.endswith("\n"):
        # Only one trailing newline allowed
        assert not raw.endswith("\n\n"), (
            f"Log file '{LOG_FILE}' has extra blank lines at the end."
        )