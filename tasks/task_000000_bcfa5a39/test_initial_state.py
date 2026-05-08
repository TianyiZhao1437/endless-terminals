# test_initial_state.py

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
    assert os.path.isdir(DOCS_DIR), f"Directory '{DOCS_DIR}' is missing. Please create it before proceeding."
    assert os.access(DOCS_DIR, os.W_OK), f"Directory '{DOCS_DIR}' is not writable. Please ensure write permissions."

@pytest.mark.order(2)
def test_ticket_resolutions_md_exists_and_content():
    assert os.path.isfile(DOC_FILE), f"Documentation file '{DOC_FILE}' is missing. Please create it before proceeding."
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize newlines for comparison
    expected = DOC_EXPECTED_CONTENT.replace("\r\n", "\n").strip()
    actual = content.replace("\r\n", "\n").strip()
    assert actual == expected, (
        f"File '{DOC_FILE}' does not match the expected content.\n"
        "Please ensure it contains the exact documentation as specified."
    )

@pytest.mark.order(3)
def test_markdown_lint_report_txt_does_not_exist_yet():
    assert not os.path.exists(REPORT_FILE), (
        f"Report file '{REPORT_FILE}' already exists. Please remove it before starting the task."
    )