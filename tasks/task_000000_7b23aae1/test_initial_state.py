# test_initial_state.py

import os
import pytest

ACCOUNT_EMAILS_PATH = "/home/user/account_emails.txt"
EMAIL_FREQUENCIES_LOG_PATH = "/home/user/email_frequencies.log"

EXPECTED_ACCOUNT_EMAILS_CONTENT = """alice@example.com
bob@example.net
carol@example.org
bob@example.net
bob@example.net
alice@example.com
bob@example.net
"""

def test_account_emails_txt_exists():
    assert os.path.isfile(ACCOUNT_EMAILS_PATH), (
        f"Required file {ACCOUNT_EMAILS_PATH} does not exist. "
        "Please ensure the file is present before starting the task."
    )

def test_account_emails_txt_content():
    with open(ACCOUNT_EMAILS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_ACCOUNT_EMAILS_CONTENT, (
        f"The file {ACCOUNT_EMAILS_PATH} does not contain the expected contents.\n"
        f"Expected:\n{EXPECTED_ACCOUNT_EMAILS_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )

def test_email_frequencies_log_does_not_exist():
    assert not os.path.exists(EMAIL_FREQUENCIES_LOG_PATH), (
        f"The file {EMAIL_FREQUENCIES_LOG_PATH} should NOT exist before you start the task."
    )