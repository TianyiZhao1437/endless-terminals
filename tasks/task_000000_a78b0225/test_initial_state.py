# test_initial_state.py

import os
import pytest

CSV_PATH = "/home/user/db_logs/slow_queries.csv"
CSV_EXPECTED = (
    "query_id,query_text,execution_time_ms,timestamp\n"
    "1,SELECT * FROM users;,150,2024-06-01T12:30:01\n"
    "2,UPDATE accounts SET balance=balance-100 WHERE id=3;,723,2024-06-01T12:35:26\n"
    "3,SELECT count(*) FROM logs WHERE severity='ERROR';,87,2024-06-01T13:00:12\n"
    "4,DELETE FROM logs WHERE date < '2024-01-01';,801,2024-06-01T13:23:37\n"
)

REPORT_PATH = "/home/user/db_logs/slow_queries_report.json"

def test_db_logs_directory_exists():
    dir_path = "/home/user/db_logs"
    assert os.path.isdir(dir_path), (
        f"Required directory '{dir_path}' does not exist. "
        "Create it before proceeding."
    )

def test_slow_queries_csv_exists_and_content():
    assert os.path.isfile(CSV_PATH), (
        f"Required file '{CSV_PATH}' does not exist. "
        "Create it with the correct contents before proceeding."
    )
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == CSV_EXPECTED, (
        f"File '{CSV_PATH}' exists but its contents are incorrect.\n"
        "Expected:\n"
        f"{CSV_EXPECTED}\n"
        "Actual:\n"
        f"{content}\n"
        "Please ensure the file contents match exactly."
    )

def test_report_json_does_not_exist_before_task():
    assert not os.path.exists(REPORT_PATH), (
        f"File '{REPORT_PATH}' should NOT exist before you perform the task. "
        "Remove it before starting."
    )