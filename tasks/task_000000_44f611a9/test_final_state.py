# test_final_state.py

import os
import pytest

INI_PATH = '/home/user/docs/config/settings.ini'
EXTRACTED_PATH = '/home/user/docs/config/doc_settings_extracted.txt'

EXPECTED_DOC_SETTINGS_EXTRACTED = (
    "intro=Getting Started Guide\n"
    "usage=How To Use The Software\n"
    "faq=Frequently Asked Questions"
)

def get_documentation_section_from_ini(ini_path):
    """
    Parse the INI file manually to extract key-value pairs from the [documentation] section,
    preserving their order and ignoring comments, section headers, and other sections.
    Returns a list of lines in 'key=value' format.
    """
    documentation_lines = []
    in_documentation = False

    with open(ini_path, encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            # Skip blank lines and comments
            if not stripped or stripped.startswith(';') or stripped.startswith('#'):
                continue
            if stripped.startswith('['):
                # Section header
                if stripped.lower() == '[documentation]':
                    in_documentation = True
                else:
                    in_documentation = False
                continue
            if in_documentation:
                # Only lines in [documentation] section, expect key=value pairs
                if '=' in stripped:
                    documentation_lines.append(stripped)
    return documentation_lines

def test_extracted_file_exists():
    assert os.path.isfile(EXTRACTED_PATH), (
        f"Missing extracted documentation settings file: {EXTRACTED_PATH}.\n"
        "After completing the task, this file must exist with the extracted [documentation] section."
    )

def test_extracted_file_content_exact():
    with open(EXTRACTED_PATH, encoding='utf-8') as f:
        content = f.read()
    # Normalize line endings and strip trailing whitespace/newlines
    normalized_actual = content.replace('\r\n', '\n').strip()
    normalized_expected = EXPECTED_DOC_SETTINGS_EXTRACTED.strip()
    assert normalized_actual == normalized_expected, (
        f"The content of {EXTRACTED_PATH} is incorrect.\n"
        "Expected EXACTLY:\n"
        f"{EXPECTED_DOC_SETTINGS_EXTRACTED}\n"
        "But got:\n"
        f"{content}\n"
        "Ensure only key=value pairs from the [documentation] section are present, "
        "in the correct order, with no extra spaces or blank lines."
    )

def test_extracted_file_order_and_no_extras():
    # Check for order and absence of extra lines/keys
    expected_lines = EXPECTED_DOC_SETTINGS_EXTRACTED.split('\n')
    actual_lines = []
    with open(EXTRACTED_PATH, encoding='utf-8') as f:
        for line in f:
            stripped = line.rstrip('\r\n')
            actual_lines.append(stripped)

    assert actual_lines == expected_lines, (
        f"The lines in {EXTRACTED_PATH} are not in the correct order or contain extra/missing lines.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}\n"
        "Check that only the documentation keys are present, in the exact order as in the INI file, "
        "with no extra blank lines or spaces."
    )

def test_extracted_file_matches_ini_documentation_section():
    # Dynamically parse the INI to get the [documentation] section and compare to output file
    expected_from_ini = get_documentation_section_from_ini(INI_PATH)
    with open(EXTRACTED_PATH, encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]
    assert actual_lines == expected_from_ini, (
        f"The extracted file does not match the [documentation] section of {INI_PATH}.\n"
        f"Expected (from INI):\n{expected_from_ini}\n"
        f"Actual (in extracted file):\n{actual_lines}\n"
        "Verify that you have extracted ONLY the [documentation] section's key-value pairs, "
        "in the same order, with no extra lines or keys."
    )