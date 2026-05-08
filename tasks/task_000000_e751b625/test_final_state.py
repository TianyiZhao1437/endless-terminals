# test_final_state.py

import os
import subprocess
import pytest

ENV_PATH = "/home/user/backup_job/.env"
EXPECTED_OUTPUT = "abc123secure"

@pytest.mark.describe("Verify .env file still exists after task completion.")
def test_env_file_still_exists():
    assert os.path.isfile(ENV_PATH), (
        f"After task completion, required .env file not found at {ENV_PATH}. "
        "The file must not be deleted or moved."
    )

@pytest.mark.describe("Verify .env file contents are unchanged after task completion.")
def test_env_file_contents_unchanged():
    try:
        with open(ENV_PATH, "r") as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {ENV_PATH}: {e}")

    expected_contents = (
        "BACKUP_PATH=/mnt/backups\n"
        "INTEGRITY_KEY=abc123secure\n"
        "LAST_RUN=2024-06-17\n"
    )
    assert contents == expected_contents, (
        f"The contents of {ENV_PATH} have changed.\n"
        f"Expected:\n{expected_contents!r}\n"
        f"Found:\n{contents!r}\n"
        "The .env file must not be modified by this task."
    )

@pytest.mark.describe("Verify that the correct command output is produced: only the INTEGRITY_KEY value, no extra text.")
def test_command_output_only_integrity_key(monkeypatch):
    """
    The student must have run a command that outputs only the value of INTEGRITY_KEY,
    with no extra whitespace or newlines, and nothing else.
    We simulate running the expected shell command here.
    """
    # The command the student should have run, for example:
    # grep '^INTEGRITY_KEY=' /home/user/backup_job/.env | cut -d= -f2
    # or
    # awk -F= '/^INTEGRITY_KEY=/{print $2}' /home/user/backup_job/.env
    # We'll simulate that by running a shell one-liner.

    # Compose a shell command that mimics the expected behaviour
    shell_cmd = (
        "awk -F= '/^INTEGRITY_KEY=/{print $2}' /home/user/backup_job/.env"
    )

    try:
        result = subprocess.run(
            shell_cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    except Exception as e:
        pytest.fail(f"Failed to run validation command: {e}")

    output = result.stdout
    # Remove only a trailing newline, but not whitespace elsewhere
    output = output.rstrip("\n")

    assert output == EXPECTED_OUTPUT, (
        "The command output is not exactly the expected INTEGRITY_KEY value.\n"
        f"Expected output: {EXPECTED_OUTPUT!r}\n"
        f"Actual output: {output!r}\n"
        "The output must be the value only, with no extra whitespace, labels, or newlines."
    )

@pytest.mark.describe("Ensure no extra files or directories are present after task completion.")
def test_no_extra_files_or_dirs():
    # The only file that should exist is /home/user/backup_job/.env
    backup_job_dir = "/home/user/backup_job"
    assert os.path.isdir(backup_job_dir), (
        f"Directory {backup_job_dir} is missing after task completion."
    )
    entries = os.listdir(backup_job_dir)
    assert entries == [".env"], (
        f"Unexpected files or directories found in {backup_job_dir} after task completion: {entries}\n"
        "There must be only the .env file present."
    )