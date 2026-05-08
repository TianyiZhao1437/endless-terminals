# test_final_state.py

import os
import pytest

DEV_PROJECT_DIR = "/home/user/dev_project"
FILENAMES_TXT = os.path.join(DEV_PROJECT_DIR, "filenames.txt")
FILENAME_COUNTS_TXT = os.path.join(DEV_PROJECT_DIR, "filename_counts.txt")

EXPECTED_COUNTS = {
    "main.py": 3,
    "README.md": 2,
    "test_utils.py": 7,
}
EXPECTED_ORDER = sorted(EXPECTED_COUNTS.keys())

@pytest.mark.final_state
def test_filename_counts_txt_exists():
    assert os.path.isfile(FILENAME_COUNTS_TXT), (
        f"Missing required output file: '{FILENAME_COUNTS_TXT}'. "
        "You must create this file with the correct counts and format."
    )

@pytest.mark.final_state
def test_filename_counts_txt_content_and_format():
    try:
        with open(FILENAME_COUNTS_TXT, "r", encoding="utf-8") as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        pytest.fail(
            f"Could not read '{FILENAME_COUNTS_TXT}': {e}. "
            "Ensure the file is readable and contains the required content."
        )

    # Check for blank lines at start or end
    if not lines:
        pytest.fail(
            f"'{FILENAME_COUNTS_TXT}' is empty. "
            "It must contain one line per unique file name, with the correct count and format."
        )
    if lines[0].strip() == "" or lines[-1].strip() == "":
        pytest.fail(
            f"'{FILENAME_COUNTS_TXT}' contains leading or trailing blank lines. "
            "Remove all blank lines; only output count/name lines."
        )

    # Check number of lines
    expected_num_lines = len(EXPECTED_COUNTS)
    if len(lines) != expected_num_lines:
        pytest.fail(
            f"'{FILENAME_COUNTS_TXT}' has {len(lines)} lines; expected {expected_num_lines} lines (one per unique file name). "
            f"Found lines:\n{lines}"
        )

    found_names = []
    for idx, line in enumerate(lines):
        # Check line format: "<count> <filename>", no extra spaces
        if line.strip() != line:
            pytest.fail(
                f"Line {idx+1} in '{FILENAME_COUNTS_TXT}' has leading or trailing spaces: '{line}'. "
                "Each line must have no leading/trailing spaces."
            )
        parts = line.split(" ")
        if len(parts) != 2:
            pytest.fail(
                f"Line {idx+1} in '{FILENAME_COUNTS_TXT}' does not contain exactly one space: '{line}'. "
                "Each line must have the format: '<count> <filename>' (exactly one space)."
            )
        count_str, name = parts
        found_names.append(name)

        # Check count is int and matches expected
        try:
            count = int(count_str)
        except ValueError:
            pytest.fail(
                f"Count on line {idx+1} in '{FILENAME_COUNTS_TXT}' is not an integer: '{count_str}'. "
                "Counts must be positive integers."
            )
        if name not in EXPECTED_COUNTS:
            pytest.fail(
                f"Unexpected file name '{name}' found on line {idx+1} in '{FILENAME_COUNTS_TXT}'. "
                f"Expected names: {sorted(EXPECTED_COUNTS.keys())}"
            )
        expected_count = EXPECTED_COUNTS[name]
        if count != expected_count:
            pytest.fail(
                f"Incorrect count for '{name}' on line {idx+1} in '{FILENAME_COUNTS_TXT}': expected {expected_count}, found {count}."
            )

    # Check ordering
    if found_names != EXPECTED_ORDER:
        pytest.fail(
            f"File names in '{FILENAME_COUNTS_TXT}' are not sorted in ascending lexical order. "
            f"Expected order: {EXPECTED_ORDER}\nFound order: {found_names}"
        )