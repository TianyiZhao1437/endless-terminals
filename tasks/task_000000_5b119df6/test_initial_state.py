# test_initial_state.py

import os
import pytest
import stat

ETL_ENV_DIR = "/home/user/etl_env"
PACKAGES_LIST_FILE = "/home/user/etl_env/packages_list.txt"

@pytest.mark.describe("Initial OS/FS state for ETL pipeline environment preparation")
def test_etl_env_directory_exists():
    """The /home/user/etl_env directory must exist before the task begins."""
    assert os.path.isdir(ETL_ENV_DIR), (
        f"Required directory '{ETL_ENV_DIR}' does not exist. "
        "Please create it before proceeding."
    )

def test_etl_env_directory_is_writable():
    """The /home/user/etl_env directory must be writable by the user."""
    # Check that the directory is writable by trying to open a temp file inside it
    if not os.path.isdir(ETL_ENV_DIR):
        pytest.skip(f"Directory '{ETL_ENV_DIR}' does not exist, skipping write test.")
    testfile = os.path.join(ETL_ENV_DIR, ".pytest_write_test")
    try:
        with open(testfile, "w") as f:
            f.write("write test")
        # Optionally, check file permissions
        st = os.stat(testfile)
        # The file should be owned by the current user and writable
        assert bool(st.st_mode & stat.S_IWUSR), (
            f"Directory '{ETL_ENV_DIR}' is not writable by the user. "
            "Please ensure you have write permissions."
        )
    except Exception as e:
        pytest.fail(
            f"Directory '{ETL_ENV_DIR}' is not writable: {e}\n"
            "Please ensure you have write permissions."
        )
    finally:
        try:
            os.remove(testfile)
        except Exception:
            pass

def test_packages_list_file_does_not_exist_yet():
    """/home/user/etl_env/packages_list.txt should not exist before the task begins."""
    assert not os.path.exists(PACKAGES_LIST_FILE), (
        f"File '{PACKAGES_LIST_FILE}' already exists. "
        "Please remove it before starting the task."
    )