# test_final_state.py

import os
import json
import pytest

CSV_PATH = "/home/user/db_logs/slow_queries.csv"
REPORT_PATH = "/home/user/db_logs/slow_queries_report.json"

CSV_EXPECTED = (
    "query_id,query_text,execution_time_ms,timestamp\n"
    "1,SELECT * FROM users;,150,2024-06-01T12:30:01\n"
    "2,UPDATE accounts SET balance=balance-100 WHERE id=3;,723,2024-06-01T12:35:26\n"
    "3,SELECT count(*) FROM logs WHERE severity='ERROR';,87,2024-06-01T13:00:12\n"
    "4,DELETE FROM logs WHERE date < '2024-01-01';,801,2024-06-01T13:23:37\n"
)

# The expected JSON, as a string, exactly as it must appear in the file.
REPORT_EXPECTED = (
    '[{"query_id":"2","execution_time_ms":723,"timestamp":"2024-06-01T12:35:26"},'
    '{"query_id":"4","execution_time_ms":801,"timestamp":"2024-06-01T13:23:37"}]'
)

def test_csv_still_exists_and_unchanged():
    assert os.path.isfile(CSV_PATH), (
        f"File '{CSV_PATH}' is missing after task. It must not be deleted."
    )
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == CSV_EXPECTED, (
        f"File '{CSV_PATH}' contents have changed after the task.\n"
        "Expected (unchanged):\n"
        f"{CSV_EXPECTED}\n"
        "Actual:\n"
        f"{content}\n"
        "Do not modify or remove the original CSV."
    )

def test_report_json_exists():
    assert os.path.isfile(REPORT_PATH), (
        f"File '{REPORT_PATH}' does not exist. "
        "You must create this file as the summary report."
    )

def test_report_json_content_exact():
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Strict check: content must match exactly, including no trailing newline, compactness, order, etc.
    assert content == REPORT_EXPECTED, (
        f"File '{REPORT_PATH}' contents are incorrect.\n"
        "Expected exactly:\n"
        f"{REPORT_EXPECTED}\n"
        "Actual:\n"
        f"{content}\n"
        "Check that:\n"
        "- Only queries with execution_time_ms > 500 are included\n"
        "- The output is a compact JSON array, with no spaces or newlines\n"
        "- The order matches the CSV\n"
        "- Only the specified keys are present and in the correct order\n"
        "- There is no trailing newline or extra characters"
    )

def test_report_json_valid_json_and_schema():
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        arr = json.loads(content)
    except Exception as e:
        pytest.fail(
            f"File '{REPORT_PATH}' is not valid JSON: {e}\n"
            f"Actual contents:\n{content}"
        )
    assert isinstance(arr, list), (
        f"File '{REPORT_PATH}' does not contain a JSON array."
    )
    # Expected output
    expected = [
        {
            "query_id": "2",
            "execution_time_ms": 723,
            "timestamp": "2024-06-01T12:35:26"
        },
        {
            "query_id": "4",
            "execution_time_ms": 801,
            "timestamp": "2024-06-01T13:23:37"
        }
    ]
    assert arr == expected, (
        f"JSON array in '{REPORT_PATH}' does not match expected data.\n"
        f"Expected:\n{expected}\nActual:\n{arr}\n"
        "Check that only the correct slow queries are present, with correct fields and types."
    )

def test_report_json_no_trailing_newline():
    with open(REPORT_PATH, "rb") as f:
        content = f.read()
    assert not content.endswith(b"\n"), (
        f"File '{REPORT_PATH}' must NOT end with a trailing newline."
    )