# test_final_state.py

import os
import pytest

ACCOUNT_EMAILS_PATH = "/home/user/account_emails.txt"
EMAIL_FREQUENCIES_LOG_PATH = "/home/user/email_frequencies.log"

EXPECTED_ACCOUNT_EMAILS_CONTENT = (
    "alice@example.com\n"
    "bob@example.net\n"
    "carol@example.org\n"
    "bob@example.net\n"
    "bob@example.net\n"
    "alice@example.com\n"
    "bob@example.net\n"
)

EXPECTED_EMAIL_FREQUENCIES_LOG_CONTENT = (
    "2 alice@example.com\n"
    "4 bob@example.net\n"
    "1 carol@example.org\n"
)

def test_account_emails_txt_still_exists():
    assert os.path.isfile(ACCOUNT_EMAILS_PATH), (
        f"Required file {ACCOUNT_EMAILS_PATH} is missing after the task. "
        "Do not remove or rename this file."
    )

def test_account_emails_txt_content_unchanged():
    with open(ACCOUNT_EMAILS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_ACCOUNT_EMAILS_CONTENT, (
        f"The file {ACCOUNT_EMAILS_PATH} was modified during the task. "
        "It must remain unchanged.\n"
        f"Expected:\n{EXPECTED_ACCOUNT_EMAILS_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )

def test_email_frequencies_log_exists():
    assert os.path.isfile(EMAIL_FREQUENCIES_LOG_PATH), (
        f"The file {EMAIL_FREQUENCIES_LOG_PATH} does not exist. "
        "You must create this file with the required contents."
    )

def test_email_frequencies_log_content_exact():
    with open(EMAIL_FREQUENCIES_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize line endings for robustness
    normalized_expected = EXPECTED_EMAIL_FREQUENCIES_LOG_CONTENT.replace('\r\n', '\n')
    normalized_actual = content.replace('\r\n', '\n')
    assert normalized_actual == normalized_expected, (
        f"The file {EMAIL_FREQUENCIES_LOG_PATH} does not have the exact expected contents.\n"
        "Each line should have the count, a space, then the email address, sorted alphabetically, one per line.\n"
        f"Expected:\n{normalized_expected!r}\n"
        f"Found:\n{normalized_actual!r}"
    )

def test_email_frequencies_log_no_extra_lines():
    with open(EMAIL_FREQUENCIES_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    expected_lines = [
        "2 alice@example.com\n",
        "4 bob@example.net\n",
        "1 carol@example.org\n",
    ]
    assert lines == expected_lines, (
        f"The file {EMAIL_FREQUENCIES_LOG_PATH} contains extra, missing, or malformed lines.\n"
        f"Expected lines:\n{expected_lines!r}\n"
        f"Found lines:\n{lines!r}"
    )