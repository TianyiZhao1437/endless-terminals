# test_initial_state.py

import os
import pytest

LOG_FILE = '/home/user/network-pip-packages.log'

def test_network_pip_packages_log_file_does_not_exist():
    """
    The pip packages log file should NOT exist before the student performs the action.
    """
    assert not os.path.exists(LOG_FILE), (
        f"The file {LOG_FILE} should NOT exist before you list the installed pip packages. "
        "Please ensure you have NOT created this file yet."
    )