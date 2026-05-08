# test_final_state.py

import os
import pytest

DEPLOYMENTS_DIR = "/home/user/deployments"
RELEASE_2_1_0_DIR = "/home/user/deployments/release_2.1.0"
CURRENT_SYMLINK = "/home/user/deployments/current"
SYMLINK_UPDATE_LOG = "/home/user/deployments/symlink_update.log"
EXPECTED_LOG_LINE = "symlink updated: current now points to release_2.1.0"


def test_deployments_directory_still_exists():
    assert os.path.isdir(DEPLOYMENTS_DIR), (
        f"Required directory missing after task: {DEPLOYMENTS_DIR}"
    )

def test_release_2_1_0_directory_still_exists():
    assert os.path.isdir(RELEASE_2_1_0_DIR), (
        f"Required release directory missing after task: {RELEASE_2_1_0_DIR}"
    )

def test_current_symlink_points_to_new_release():
    assert os.path.lexists(CURRENT_SYMLINK), (
        f"Symlink missing after task: {CURRENT_SYMLINK}"
    )
    assert os.path.islink(CURRENT_SYMLINK), (
        f"{CURRENT_SYMLINK} exists but is not a symbolic link after the task."
    )
    target = os.readlink(CURRENT_SYMLINK)
    # Accept both absolute and relative symlinks, but must resolve to RELEASE_2_1_0_DIR
    abs_target = os.path.abspath(os.path.join(os.path.dirname(CURRENT_SYMLINK), target))
    expected_abs = os.path.abspath(RELEASE_2_1_0_DIR)
    assert abs_target == expected_abs, (
        f"{CURRENT_SYMLINK} points to {target} (resolved as {abs_target}), "
        f"but it must point to {expected_abs} after the task."
    )

def test_symlink_update_log_exists_and_content():
    assert os.path.isfile(SYMLINK_UPDATE_LOG), (
        f"Log file missing after task: {SYMLINK_UPDATE_LOG}"
    )
    with open(SYMLINK_UPDATE_LOG, "rb") as f:
        log_bytes = f.read()
    try:
        log_text = log_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(
            f"{SYMLINK_UPDATE_LOG} is not valid UTF-8 text."
        )
    # Check for exactly one line, with no extra newlines or whitespace
    # Accept a single trailing '\n', but not more, and not a missing newline
    if log_text == EXPECTED_LOG_LINE:
        pass  # Acceptable: no trailing newline
    elif log_text == EXPECTED_LOG_LINE + "\n":
        pass  # Acceptable: exactly one trailing newline
    else:
        # Explain what is wrong
        # Show the repr to make invisible characters evident
        pytest.fail(
            f"{SYMLINK_UPDATE_LOG} content is incorrect.\n"
            f"Expected exactly:\n    {repr(EXPECTED_LOG_LINE)}\n"
            f"or with a single trailing newline:\n    {repr(EXPECTED_LOG_LINE + chr(10))}\n"
            f"But got:\n    {repr(log_text)}"
        )
    # Also ensure the log file contains only this line (no extra lines)
    if log_text.endswith("\n"):
        lines = log_text.splitlines()
        assert len(lines) == 1, (
            f"{SYMLINK_UPDATE_LOG} should contain exactly one line, found {len(lines)} lines."
        )
        assert lines[0] == EXPECTED_LOG_LINE, (
            f"{SYMLINK_UPDATE_LOG} contains wrong content: {repr(lines[0])}, "
            f"expected: {repr(EXPECTED_LOG_LINE)}"
        )
    else:
        # No trailing newline, so splitlines yields one line
        assert log_text == EXPECTED_LOG_LINE, (
            f"{SYMLINK_UPDATE_LOG} contains wrong content: {repr(log_text)}, "
            f"expected: {repr(EXPECTED_LOG_LINE)}"
        )