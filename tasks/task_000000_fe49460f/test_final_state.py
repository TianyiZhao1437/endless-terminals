# test_final_state.py

import os
import pytest

HOME = "/home/user"
ETL_DIR = os.path.join(HOME, "etl_raw_data")
SCRAPED_FILE = os.path.join(ETL_DIR, "scraped_examplecom.txt")

# The exact visible text content as rendered by a text-based browser on https://example.com
TRUTH_TEXT = (
    "Example Domain\n"
    "\n"
    "This domain is for use in illustrative examples in documents. You may use this\n"
    "domain in literature without prior coordination or asking for permission.\n"
    "\n"
    "More information...\n"
)

def test_etl_raw_data_dir_exists_and_is_dir():
    """The /home/user/etl_raw_data directory must exist and be a directory."""
    assert os.path.exists(ETL_DIR), (
        f"Directory {ETL_DIR} does not exist. "
        "You must create this directory before writing the output file."
    )
    assert os.path.isdir(ETL_DIR), (
        f"{ETL_DIR} exists but is not a directory."
    )

def test_scraped_file_exists_and_is_file():
    """The scraped_examplecom.txt file must exist and be a regular file."""
    assert os.path.exists(SCRAPED_FILE), (
        f"File {SCRAPED_FILE} does not exist. "
        "You must extract the visible text and write it to this file."
    )
    assert os.path.isfile(SCRAPED_FILE), (
        f"{SCRAPED_FILE} exists but is not a regular file."
    )

def test_scraped_file_content_exact():
    """The content of the scraped_examplecom.txt file must match exactly the required visible text."""
    with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == TRUTH_TEXT, (
        f"The content of {SCRAPED_FILE} does not match the expected text.\n"
        "Expected:\n"
        f"{'-'*40}\n{TRUTH_TEXT!r}\n{'-'*40}\n"
        "Found:\n"
        f"{'-'*40}\n{content!r}\n{'-'*40}\n"
        "Check for missing/extra lines, incorrect line breaks, or stray whitespace."
    )

def test_etl_raw_data_dir_contains_only_scraped_file():
    """The /home/user/etl_raw_data directory must contain only scraped_examplecom.txt, nothing else."""
    files = os.listdir(ETL_DIR)
    assert files == ["scraped_examplecom.txt"], (
        f"{ETL_DIR} contains unexpected files or directories: {files}.\n"
        "It must contain only 'scraped_examplecom.txt'."
    )

def test_no_other_files_created(tmp_path):
    """No other files or directories should be created under /home/user except etl_raw_data/scraped_examplecom.txt."""
    allowed = {ETL_DIR}
    # List all items in /home/user (including etl_raw_data)
    all_items = {os.path.join(HOME, d) for d in os.listdir(HOME)}
    extra_items = all_items - allowed
    assert not extra_items, (
        f"Unexpected files or directories found in {HOME}: {extra_items}.\n"
        "Only 'etl_raw_data' directory should be present after the task."
    )
    # Already checked contents of etl_raw_data above