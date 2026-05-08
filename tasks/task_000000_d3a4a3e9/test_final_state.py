# test_final_state.py

import os
import pytest

ARCHIVE_DIR = '/home/user/archive'
FILE_LIST_PATH = '/home/user/archive/file_list.txt'
EXT_REPORT_PATH = '/home/user/archive/extension_report.txt'

EXPECTED_REPORT_LINES = [
    "csv 3",
    "jpg 2",
    "pdf 2",
    "txt 2",
    "zip 2",
]

@pytest.mark.describe("Final OS/filesystem state after archive extension summary task")
def test_extension_report_exists():
    assert os.path.isfile(EXT_REPORT_PATH), (
        f"Expected output file '{EXT_REPORT_PATH}' does not exist.\n"
        "You must create this file with the correct frequency report."
    )

def test_extension_report_contents_exact():
    """
    Check that /home/user/archive/extension_report.txt exists and contains exactly the correct lines:
    - One line per extension, in the format '<extension> <count>'
    - Lines sorted alphabetically by extension.
    - No extra or missing lines.
    - No extra whitespace.
    """
    with open(EXT_REPORT_PATH, 'r', encoding='utf-8') as f:
        actual_lines = [line.rstrip('\n') for line in f]

    assert actual_lines == EXPECTED_REPORT_LINES, (
        f"File '{EXT_REPORT_PATH}' contents are incorrect.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_REPORT_LINES) +
        "\nActual lines:\n"
        + "\n".join(actual_lines) +
        "\n\n"
        "Check that:\n"
        "- Each line is in the format '<extension> <count>' (e.g., 'csv 3').\n"
        "- There are no extra or missing lines.\n"
        "- The lines are sorted alphabetically by extension.\n"
        "- There is no extra whitespace or blank lines.\n"
    )

def test_extension_report_no_extra_blank_lines():
    """
    Check that there are no extra blank lines at the end or inside the report.
    """
    with open(EXT_REPORT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        assert line.strip() != '', (
            f"Blank line found in '{EXT_REPORT_PATH}' at line {i+1}. "
            "Remove all blank lines. Only extension frequency lines should be present."
        )

def test_extension_report_file_permissions():
    """
    Check that the report file is readable (by user) and not world-writable.
    """
    stat = os.stat(EXT_REPORT_PATH)
    # Owner can read/write, group and others can read only (e.g., 644)
    mode = stat.st_mode & 0o777
    assert mode & 0o400, (
        f"File '{EXT_REPORT_PATH}' is not readable by the owner. "
        "Set permissions to allow owner read access."
    )
    assert not (mode & 0o002), (
        f"File '{EXT_REPORT_PATH}' is world-writable. "
        "Remove world-writable permissions for security."
    )

def test_file_list_untouched():
    """
    Ensure the original file list is unmodified.
    """
    expected_lines = [
        "data.csv",
        "report.pdf",
        "notes.txt",
        "data.csv",
        "image.jpg",
        "slides.pdf",
        "archive.zip",
        "notes.txt",
        "data.csv",
        "photo.jpg",
        "backup.zip",
    ]
    assert os.path.isfile(FILE_LIST_PATH), (
        f"Input file '{FILE_LIST_PATH}' is missing after task. "
        "Do not remove or overwrite this file."
    )
    with open(FILE_LIST_PATH, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == expected_lines, (
        f"File '{FILE_LIST_PATH}' was modified during the task.\n"
        f"Expected lines:\n{expected_lines}\nActual lines:\n{lines}\n"
        "Do not change the input file."
    )