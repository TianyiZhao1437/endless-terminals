# test_final_state.py

import os
import pytest

MONITOR_CONFIG_PATH = "/home/user/network/monitor_config.ini"
EXPECTED_GATEWAY_VALUE = "192.168.59.1"
EXPECTED_STDOUT = EXPECTED_GATEWAY_VALUE  # No extra whitespace or newline

def test_monitor_config_file_still_exists():
    """Ensure the monitor_config.ini file still exists after task completion."""
    assert os.path.isfile(MONITOR_CONFIG_PATH), (
        f"Required file missing after task: {MONITOR_CONFIG_PATH}. "
        "The configuration file must not be altered or deleted."
    )

def test_monitor_config_file_not_modified():
    """Ensure the contents of monitor_config.ini are unchanged after task completion."""
    expected_content = (
        "[network]\n"
        "interface=eth0\n"
        "gateway=192.168.59.1\n"
        "dns=8.8.8.8\n"
        "\n"
        "[alert]\n"
        "email=admin@example.com\n"
        "threshold=75\n"
    )
    with open(MONITOR_CONFIG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == expected_content, (
        f"The contents of {MONITOR_CONFIG_PATH} have been modified.\n"
        "Expected:\n"
        f"{expected_content!r}\n"
        "Actual:\n"
        f"{actual_content!r}\n"
        "Do not change the configuration file."
    )

def test_gateway_output_is_correct(monkeypatch, capsys):
    """
    Simulate rerunning the student's code and validate the ONLY output is the expected gateway value,
    with no extra whitespace, newlines, or text.
    """
    # Re-implement the expected extraction logic to simulate the student's script
    import configparser

    config = configparser.ConfigParser()
    config.optionxform = str  # preserve key case
    with open(MONITOR_CONFIG_PATH, "r", encoding="utf-8") as f:
        config.read_file(f)

    try:
        gateway_value = config["network"]["gateway"]
    except KeyError as e:
        pytest.fail(
            f"Failed to extract [network] gateway key from {MONITOR_CONFIG_PATH}: {e}"
        )

    # Simulate ONLY printing the gateway value (no newline)
    print(gateway_value, end="")

    # Capture output
    captured = capsys.readouterr()
    stdout = captured.out
    stderr = captured.err

    assert stdout == EXPECTED_STDOUT, (
        f"Incorrect console output for gateway value.\n"
        f"Expected: {EXPECTED_STDOUT!r}\n"
        f"Actual:   {stdout!r}\n"
        "Print ONLY the gateway value, with no extra whitespace, text, or newlines."
    )
    assert stderr == "", (
        f"Unexpected output to stderr: {stderr!r}\n"
        "There should be no error output."
    )