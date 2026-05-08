# test_initial_state.py

import os
import pytest

MONITORING_DIR = "/home/user/monitoring_logs"
APP_LOG = "/home/user/monitoring_logs/app.log"
ALERTS_SUMMARY = "/home/user/monitoring_logs/alerts_summary.txt"

EXPECTED_APP_LOG_CONTENT = (
    "2024-06-15 08:23:40 INFO Starting application\n"
    "2024-06-15 08:23:41 CRITICAL Database connection lost\n"
    "2024-06-15 08:24:00 ERROR Failed to load configuration file\n"
    "2024-06-15 08:25:00 INFO Application shut down\n"
    "2024-06-15 08:26:00 WARNING Low memory detected\n"
)

def test_monitoring_directory_exists():
    assert os.path.isdir(MONITORING_DIR), (
        f"Required directory does not exist: {MONITORING_DIR}"
    )

def test_app_log_file_exists():
    assert os.path.isfile(APP_LOG), (
        f"Required log file does not exist: {APP_LOG}"
    )

def test_app_log_file_contents():
    try:
        with open(APP_LOG, "r", encoding="utf-8") as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {APP_LOG}: {e}")

    assert contents == EXPECTED_APP_LOG_CONTENT, (
        f"{APP_LOG} does not match the expected contents.\n"
        f"--- Expected ---\n{EXPECTED_APP_LOG_CONTENT!r}\n"
        f"--- Found ---\n{contents!r}"
    )

def test_alerts_summary_does_not_exist():
    assert not os.path.exists(ALERTS_SUMMARY), (
        f"{ALERTS_SUMMARY} should not exist before the task is performed."
    )