# test_initial_state.py

import os
import pytest

HOME = "/home/user"
ENV_FILE = os.path.join(HOME, ".pg_backup.env")
COMMAND_LOG = os.path.join(HOME, "backup_command.log")

@pytest.mark.parametrize("path", [ENV_FILE, COMMAND_LOG])
def test_files_do_not_exist_initially(path):
    """
    Before the student begins the task, neither .pg_backup.env nor backup_command.log should exist.
    """
    assert not os.path.exists(path), (
        f"File or directory '{path}' should NOT exist before you begin the task. "
        f"Please start with a clean state."
    )