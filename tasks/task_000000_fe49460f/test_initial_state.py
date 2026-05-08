# test_initial_state.py

import os
import pytest

HOME = "/home/user"
ETL_DIR = os.path.join(HOME, "etl_raw_data")
SCRAPED_FILE = os.path.join(ETL_DIR, "scraped_examplecom.txt")


def test_etl_raw_data_dir_not_present():
    """The /home/user/etl_raw_data directory should NOT exist before the task begins."""
    assert not os.path.exists(ETL_DIR), (
        f"Directory {ETL_DIR} should NOT exist before starting the task. "
        "It must be created by your solution."
    )


def test_scraped_file_not_present():
    """The scraped_examplecom.txt file should NOT exist before the task begins."""
    assert not os.path.exists(SCRAPED_FILE), (
        f"File {SCRAPED_FILE} should NOT exist before starting the task. "
        "It must be created by your solution."
    )