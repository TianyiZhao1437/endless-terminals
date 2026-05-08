# test_initial_state.py

import os
import pytest

HOME = '/home/user'
MEMORY_LOG_PATH = os.path.join(HOME, 'memory_check.log')

def test_memory_check_log_does_not_exist():
    """
    The output file /home/user/memory_check.log must NOT exist before the student performs the action.
    """
    assert not os.path.exists(MEMORY_LOG_PATH), (
        f"The file {MEMORY_LOG_PATH} should NOT exist before you run the memory statistics command."
    )