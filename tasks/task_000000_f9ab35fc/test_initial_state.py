# test_initial_state.py

import os
import pytest

SETTINGS_INI_PATH = "/home/user/build_pipeline/settings.ini"


def test_settings_ini_exists():
    """Check that the settings.ini file exists at the expected path."""
    assert os.path.isfile(SETTINGS_INI_PATH), (
        f"Missing required file: {SETTINGS_INI_PATH}\n"
        f"Please ensure the configuration file exists at the specified location."
    )


def test_settings_ini_content():
    """Check that the settings.ini file has the required content and structure."""
    expected_content = (
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

    try:
        with open(SETTINGS_INI_PATH, "r", encoding="utf-8") as f:
            actual_content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {SETTINGS_INI_PATH}: {e}")

    assert actual_content == expected_content, (
        f"The file {SETTINGS_INI_PATH} does not match the expected content.\n"
        f"--- Expected content ---\n{expected_content}\n"
        f"--- Actual content ---\n{actual_content}\n"
        f"Ensure there are no extra or missing lines, whitespace, or sections."
    )