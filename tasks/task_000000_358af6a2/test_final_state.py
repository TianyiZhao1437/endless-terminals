# test_final_state.py

import os
import pytest

EXTRACTED_IDS_PATH = "/home/user/extracted_ids.txt"

# The expected exact final content of /home/user/extracted_ids.txt
EXPECTED_EXTRACTED_IDS_CONTENT = "12\n42\n77\n"

def test_extracted_ids_file_exists():
    assert os.path.isfile(EXTRACTED_IDS_PATH), (
        f"Expected output file {EXTRACTED_IDS_PATH} does not exist.\n"
        "You must create this file as part of the task."
    )

def test_extracted_ids_file_content_exact():
    with open(EXTRACTED_IDS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_EXTRACTED_IDS_CONTENT, (
        f"The file {EXTRACTED_IDS_PATH} does not contain the expected extracted id values.\n"
        "Expected exactly:\n"
        f"{EXPECTED_EXTRACTED_IDS_CONTENT!r}\n"
        "But got:\n"
        f"{content!r}\n"
        "Ensure that:\n"
        "- Only lines with an 'id' key are included\n"
        "- Each id value appears on its own line, in order\n"
        "- There are no blank lines, extra whitespace, or extra characters\n"
        "- No commas, spaces, or other delimiters are present\n"
        "- The file ends with a single newline"
    )

def test_extracted_ids_file_no_extra_lines_or_spaces():
    with open(EXTRACTED_IDS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove trailing newlines for analysis
    stripped_lines = [line.rstrip('\n\r') for line in lines]

    # Check for blank lines or lines with whitespace
    for i, line in enumerate(stripped_lines, 1):
        assert line.strip() == line, (
            f"Line {i} in {EXTRACTED_IDS_PATH!r} contains unexpected leading/trailing whitespace: {repr(line)}"
        )
        assert line != "", (
            f"Line {i} in {EXTRACTED_IDS_PATH!r} is blank. There should be no blank lines."
        )

    # Check that only digits are present on each line (no spaces, no letters, no punctuation)
    for i, line in enumerate(stripped_lines, 1):
        assert line.isdigit(), (
            f"Line {i} in {EXTRACTED_IDS_PATH!r} must contain only the id number, but got: {repr(line)}"
        )

def test_extracted_ids_file_order():
    # Check that the IDs are in the expected order
    with open(EXTRACTED_IDS_PATH, "r", encoding="utf-8") as f:
        ids = [line.strip() for line in f if line.strip()]
    expected_order = ["12", "42", "77"]
    assert ids == expected_order, (
        f"The id values in {EXTRACTED_IDS_PATH!r} are not in the expected order.\n"
        f"Expected order: {expected_order}\n"
        f"Actual order:   {ids}\n"
        "Ensure you write the ids in the order their lines appear in the input file."
    )