# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/mlops_experiments.db"
LOG_PATH = "/home/user/artifact_log.txt"

# The expected output as produced by the sqlite3 CLI in column mode for the SELECT statement.
EXPECTED_LOG_CONTENT = (
    "id          experiment_name  artifact_path                   created_at          \n"
    "----------  ---------------  ------------------------------  -------------------\n"
    "1           exp_alpha        /home/user/artifacts/model_v1.pkl 2024-06-15T14:32:00\n"
)

@pytest.mark.describe("Check the SQLite database file exists at the correct location")
def test_database_file_exists():
    assert os.path.isfile(DB_PATH), (
        f"Expected SQLite database file at '{DB_PATH}' but it does not exist."
    )

@pytest.mark.describe("Check the 'artifacts' table exists with correct columns and types")
def test_artifacts_table_schema():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.execute("PRAGMA table_info(artifacts)")
        columns = cur.fetchall()
    finally:
        con.close()

    # Expected columns: (cid, name, type, notnull, dflt_value, pk)
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "experiment_name", "TEXT", 1, None, 0),
        (2, "artifact_path", "TEXT", 1, None, 0),
        (3, "created_at", "TEXT", 1, None, 0),
    ]
    # Only compare the relevant fields: (cid, name, type, notnull, dflt_value, pk)
    assert len(columns) == len(expected_columns), (
        f"'artifacts' table should have {len(expected_columns)} columns, found {len(columns)}."
    )
    for idx, (actual, expected) in enumerate(zip(columns, expected_columns)):
        assert actual[:6] == expected, (
            f"Column {idx} expected {expected}, but got {actual}."
        )

@pytest.mark.describe("Check that the 'artifacts' table contains exactly the expected row")
def test_artifacts_table_single_row():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.execute(
            "SELECT id, experiment_name, artifact_path, created_at FROM artifacts"
        )
        rows = cur.fetchall()
    finally:
        con.close()

    assert len(rows) == 1, (
        f"'artifacts' table should contain exactly 1 row, found {len(rows)}."
    )
    expected_row = (
        1,
        "exp_alpha",
        "/home/user/artifacts/model_v1.pkl",
        "2024-06-15T14:32:00"
    )
    assert rows[0] == expected_row, (
        f"The row in 'artifacts' table is {rows[0]}, but expected {expected_row}."
    )

@pytest.mark.describe("Check that the artifact log file exists and has the correct SELECT output")
def test_artifact_log_file_content():
    assert os.path.isfile(LOG_PATH), (
        f"Expected log file '{LOG_PATH}' to exist, but it does not."
    )
    with open(LOG_PATH, "rt", encoding="utf-8") as f:
        content = f.read()
    if content != EXPECTED_LOG_CONTENT:
        # Show a helpful diff for debugging
        import difflib
        diff = "\n".join(difflib.unified_diff(
            EXPECTED_LOG_CONTENT.splitlines(),
            content.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        ))
        pytest.fail(
            f"Log file '{LOG_PATH}' does not match expected sqlite3 column output.\n"
            f"--- Diff (expected vs actual): ---\n{diff}"
        )

@pytest.mark.describe("Check that only the expected table exists in the database")
def test_only_artifacts_table_exists():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [row[0] for row in cur.fetchall()]
    finally:
        con.close()
    assert tables == ["artifacts"], (
        f"Expected only one table named 'artifacts' in the database, found: {tables}"
    )