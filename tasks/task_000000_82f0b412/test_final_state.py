# test_final_state.py

import pytest
import os

LOGS_DIR = "/home/user/logs"
LOG_FILE = "/home/user/logs/dashboard_events.log"
OUTPUT_FILE = "/home/user/logs/unique_services.txt"

EXPECTED_UNIQUE_SERVICES = ["api", "db", "frontend"]

def test_logs_directory_still_exists():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory '{LOGS_DIR}' is missing after task completion. "
        "The directory must not be deleted or moved."
    )

def test_dashboard_events_log_unchanged():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' is missing after task completion. "
        "The log file must not be deleted or moved."
    )
    expected_content = [
        "[2024-05-01T12:00:00Z] SERVICE=api EVENT=restarted",
        "[2024-05-01T12:01:00Z] SERVICE=db EVENT=healthy",
        "[2024-05-01T12:02:00Z] SERVICE=api EVENT=scaling",
        "[2024-05-01T12:03:00Z] SERVICE=frontend EVENT=deployed",
        "[2024-05-01T12:04:00Z] SERVICE=db EVENT=backup",
    ]
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip() for line in f.readlines()]
    assert actual_lines == expected_content, (
        f"Log file '{LOG_FILE}' was modified. It must remain exactly as originally provided.\n"
        "Expected content:\n" + "\n".join(expected_content)
    )

def test_unique_services_txt_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"Output file '{OUTPUT_FILE}' was not created. "
        "You must generate this file by extracting unique service names from the log."
    )

def test_unique_services_txt_content():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    assert lines == EXPECTED_UNIQUE_SERVICES, (
        f"Output file '{OUTPUT_FILE}' does not contain the correct unique service names.\n"
        "Expected one service name per line, sorted alphabetically, with no extra text or blank lines.\n"
        "Expected:\n" + "\n".join(EXPECTED_UNIQUE_SERVICES) +
        "\nActual:\n" + "\n".join(lines)
    )

def test_unique_services_txt_no_extra_blank_lines():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    # Check for trailing blank lines
    if raw.endswith("\n"):
        trailing = raw[len(raw.rstrip("\n")):]
        num_trailing = trailing.count("\n")
        assert num_trailing == 1, (
            f"Output file '{OUTPUT_FILE}' contains extra blank lines at the end. "
            "There must be no extra blank lines after the last service name."
        )

def test_unique_services_txt_no_headers():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    disallowed_headers = {"service", "services", "unique_services", "header"}
    first_line = lines[0] if lines else ""
    assert first_line not in disallowed_headers, (
        f"Output file '{OUTPUT_FILE}' contains a header or extra text ('{first_line}'). "
        "Only service names should be written, one per line, with no headers."
    )

def test_unique_services_txt_overwritten(tmp_path):
    """
    If the output file existed before, it must be overwritten.
    This test simulates by writing dummy content and checks that after task completion,
    the file contains only the expected lines.
    """
    dummy_content = "dummy_service\n"
    # Write dummy content to the output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(dummy_content)
    # Re-run extraction (student's task should have done this)
    # Now check that dummy content is gone and only expected content is present
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    assert lines == EXPECTED_UNIQUE_SERVICES, (
        f"Output file '{OUTPUT_FILE}' was not properly overwritten. "
        "It must contain only the expected unique service names, with no leftover or old content."
    )