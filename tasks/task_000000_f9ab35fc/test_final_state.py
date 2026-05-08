# test_final_state.py

import os
import pytest

SETTINGS_INI_PATH = "/home/user/build_pipeline/settings.ini"
LOG_PATH = "/home/user/build_pipeline/build_settings.log"

EXPECTED_SETTINGS_INI = (
    "[Release]\n"
    "version=1.2.3\n"
    "timestamp=2024-06-15\n\n"
    "[Android]\n"
    "minSdk=21\n"
    "targetSdk=33\n\n"
    "[iOS]\n"
    "exportSymbols=true\n"
    "archs=arm64\n"
)

EXPECTED_LOG_CONTENT = (
    "release_version=1.2.3\n"
    "android_min_sdk=21\n"
    "ios_export_symbols=true"
)

def test_settings_ini_unchanged():
    """Ensure settings.ini still exists and is exactly as expected after the task."""
    assert os.path.isfile(SETTINGS_INI_PATH), (
        f"settings.ini is missing at {SETTINGS_INI_PATH} after the task.\n"
        f"Do not remove or move the original configuration file."
    )
    with open(SETTINGS_INI_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    assert actual == EXPECTED_SETTINGS_INI, (
        f"settings.ini was modified after the task.\n"
        f"--- Expected content ---\n{EXPECTED_SETTINGS_INI}\n"
        f"--- Actual content ---\n{actual}\n"
        f"Do not change the configuration file."
    )

def test_build_settings_log_exists():
    """Check that the build_settings.log file exists after the task."""
    assert os.path.isfile(LOG_PATH), (
        f"build_settings.log was not created at {LOG_PATH}.\n"
        f"Make sure you write the extracted settings to the correct path."
    )

def test_build_settings_log_content():
    """Check that build_settings.log contains exactly the expected lines, in order, with no extra whitespace."""
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    stripped_lines = [line.rstrip('\n') for line in lines]

    expected_lines = EXPECTED_LOG_CONTENT.split('\n')

    # Check for extra/missing lines
    assert len(stripped_lines) == 3, (
        f"build_settings.log must contain exactly 3 lines but has {len(stripped_lines)}.\n"
        f"--- Actual content ---\n{''.join(lines)}"
    )

    # Check for exact content and order
    for i, (actual, expected) in enumerate(zip(stripped_lines, expected_lines), start=1):
        assert actual == expected, (
            f"Line {i} of build_settings.log is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Ensure the format, order, and values are exactly as specified, with no extra whitespace."
        )

def test_build_settings_log_no_extra_whitespace():
    """Ensure there is no extra whitespace at the end or within lines in build_settings.log."""
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for trailing whitespace
    assert content == EXPECTED_LOG_CONTENT, (
        f"build_settings.log contains extra whitespace or blank lines.\n"
        f"--- Expected content ---\n{EXPECTED_LOG_CONTENT!r}\n"
        f"--- Actual content ---\n{content!r}\n"
        f"Ensure there are no extra spaces or blank lines before, after, or between the lines."
    )