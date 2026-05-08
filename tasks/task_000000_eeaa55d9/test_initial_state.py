# test_initial_state.py

import os
import pytest

NETWORK_TEST_DIR = "/home/user/network_test"

def test_network_test_directory_does_not_exist():
    assert not os.path.exists(NETWORK_TEST_DIR), (
        f"The directory '{NETWORK_TEST_DIR}' should NOT exist before you begin. "
        "Please ensure the initial state is clean."
    )