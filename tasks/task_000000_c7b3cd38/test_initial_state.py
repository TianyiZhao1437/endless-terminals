# test_initial_state.py

import os
import pytest
import pwd

DEVTOOLS_DIR = "/home/user/devtools"

def test_devtools_directory_exists():
    assert os.path.isdir(DEVTOOLS_DIR), (
        f"The directory '{DEVTOOLS_DIR}' does not exist. "
        "Please ensure it is created before proceeding."
    )

def test_devtools_directory_owned_by_user():
    stat_info = os.stat(DEVTOOLS_DIR)
    try:
        owner_name = pwd.getpwuid(stat_info.st_uid).pw_name
    except KeyError:
        owner_name = None
    assert owner_name == "user", (
        f"The directory '{DEVTOOLS_DIR}' is not owned by 'user'. "
        f"Current owner: '{owner_name}'. Please correct the ownership."
    )