# test_initial_state.py

import os
import stat
import pytest

DB_CONFIG_DIR = "/home/user/db_config"

def test_db_config_directory_exists():
    assert os.path.exists(DB_CONFIG_DIR), (
        f"Directory '{DB_CONFIG_DIR}' does not exist. "
        "Create this directory before proceeding."
    )
    assert os.path.isdir(DB_CONFIG_DIR), (
        f"'{DB_CONFIG_DIR}' exists but is not a directory."
    )

def test_db_config_directory_is_writable():
    # Check if the directory is writable by the current user
    if not os.access(DB_CONFIG_DIR, os.W_OK):
        # Check permissions bits
        st = os.stat(DB_CONFIG_DIR)
        mode = st.st_mode
        uid = os.getuid()
        gid = os.getgid()
        if st.st_uid == uid and mode & stat.S_IWUSR:
            writable = True
        elif st.st_gid == gid and mode & stat.S_IWGRP:
            writable = True
        elif mode & stat.S_IWOTH:
            writable = True
        else:
            writable = False
        assert writable, (
            f"Directory '{DB_CONFIG_DIR}' is not writable by the current user. "
            "Adjust permissions before proceeding."
        )
    else:
        # os.access returned True, so it's writable
        pass

def test_env_file_does_not_exist():
    env_path = os.path.join(DB_CONFIG_DIR, ".env")
    assert not os.path.exists(env_path), (
        f"File '{env_path}' already exists. The initial state must not contain this file."
    )

def test_query_optimization_log_does_not_exist():
    log_path = os.path.join(DB_CONFIG_DIR, "query_optimization.log")
    assert not os.path.exists(log_path), (
        f"File '{log_path}' already exists. The initial state must not contain this file."
    )