# test_final_state.py

import os
import pytest

DOCS_DIR = "/home/user/support_docs"
DOC_FILE = os.path.join(DOCS_DIR, "ticket_resolutions.md")
REPORT_FILE = os.path.join(DOCS_DIR, "markdown_lint_report.txt")

DOC_EXPECTED_CONTENT = """# Password Reset

Steps to resolve:
1. Verified user identity via security questions.
2. Used the password reset tool to issue a temporary password.
3. Instructed user to change password upon next login.

# Printer Not Connecting

Steps to resolve:
1. Confirmed printer is powered on and connected to network.
2. Reinstalled printer drivers on the user's computer.
3. Sent test print — successful.

# VPN Configuration

Steps to resolve:
1. Provided correct VPN client download link.
2. Guided user through installation and credential entry.
3. Verified successful VPN connection with user.
"""

LINT_EXPECTED_LINES = [
    "/home/user/support_docs/ticket_resolutions.md:3 MD032 Lists should be surrounded by blank lines",
    "/home/user/support_docs/ticket_resolutions.md:10 MD032 Lists should be surrounded by blank lines",
    "/home/user/support_docs/ticket_resolutions.md:17 MD032 Lists should be surrounded by blank lines",
]

@pytest.mark.order(1)
def test_support_docs_dir_exists_and_writable():
    assert os.path.isdir(DOCS_DIR), f"Directory '{DOCS_DIR}' is missing. It must exist."
    assert os.access(DOCS_DIR, os.W_OK), f"Directory '{DOCS_DIR}' is not writable. Please fix permissions."

@pytest.mark.order(2)
def test_ticket_resolutions_md_exists_and_content():
    assert os.path.isfile(DOC_FILE), f"Documentation file '{DOC_FILE}' is missing."
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    expected = DOC_EXPECTED_CONTENT.replace("\r\n", "\n").strip()
    actual = content.replace("\r\n", "\n").strip()
    assert actual == expected, (
        f"File '{DOC_FILE}' does not match the expected documentation content."
    )

@pytest.mark.order(3)
def test_markdown_lint_report_exists_and_is_file():
    assert os.path.isfile(REPORT_FILE), (
        f"Markdown lint report file '{REPORT_FILE}' is missing. "
        "You must produce this file as output of the linter."
    )

@pytest.mark.order(4)
def test_markdown_lint_report_content_exact():
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip only the trailing newline for comparison, but do not strip whitespace
    lines = [line.rstrip('\n') for line in lines]

    assert len(lines) == len(LINT_EXPECTED_LINES), (
        f"Markdown lint report '{REPORT_FILE}' should have exactly {len(LINT_EXPECTED_LINES)} lines, "
        f"but has {len(lines)} lines.\n"
        f"Expected lines:\n" + "\n".join(LINT_EXPECTED_LINES) +
        f"\nActual lines:\n" + "\n".join(lines)
    )

    for i, (actual, expected) in enumerate(zip(lines, LINT_EXPECTED_LINES), 1):
        assert actual == expected, (
            f"Line {i} in '{REPORT_FILE}' is incorrect.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            "Each line must match the format: "
            "FILENAME:LINE_NUMBER RULE_NAME MESSAGE"
        )

@pytest.mark.order(5)
def test_markdown_lint_report_line_endings():
    # Ensure UNIX newlines only
    with open(REPORT_FILE, "rb") as f:
        data = f.read()
    if b"\r\n" in data:
        raise AssertionError(
            f"File '{REPORT_FILE}' contains Windows-style (CRLF) line endings. "
            "Please ensure all lines end with a UNIX newline (\\n) only."
        )
    if not data.endswith(b"\n"):
        raise AssertionError(
            f"File '{REPORT_FILE}' does not end with a newline character. "
            "The file must end with a single UNIX newline."
        )