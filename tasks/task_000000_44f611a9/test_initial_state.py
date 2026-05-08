# test_initial_state.py

import os
import pytest

INI_PATH = '/home/user/docs/config/settings.ini'
EXTRACTED_PATH = '/home/user/docs/config/doc_settings_extracted.txt'

EXPECTED_INI_CONTENT = """[general]
version=2.3
author=Sam Doe

[documentation]
intro=Getting Started Guide
usage=How To Use The Software
faq=Frequently Asked Questions

[network]
port=8080
timeout=60
"""

def test_ini_file_exists():
    assert os.path.isfile(INI_PATH), (
        f"Missing INI file: {INI_PATH}.\n"
        "Expected to find the configuration file with documentation settings."
    )

def test_ini_file_content():
    with open(INI_PATH, encoding='utf-8') as f:
        content = f.read()
    # Normalize line endings for comparison
    normalized_actual = content.replace('\r\n', '\n').strip()
    normalized_expected = EXPECTED_INI_CONTENT.strip()
    assert normalized_actual == normalized_expected, (
        f"INI file at {INI_PATH} does not have the expected content.\n"
        "Expected content:\n"
        f"{EXPECTED_INI_CONTENT}\n"
        "Actual content:\n"
        f"{content}\n"
        "Ensure the [documentation] section and other sections are present as described."
    )

def test_extracted_file_does_not_exist_yet():
    assert not os.path.exists(EXTRACTED_PATH), (
        f"The output file {EXTRACTED_PATH} already exists before extraction. "
        "It should not exist prior to performing the extraction task."
    )