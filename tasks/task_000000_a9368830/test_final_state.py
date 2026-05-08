# test_final_state.py

import os
import stat
import pytest
import re

CSV_PATH = "/home/user/applications/profile_log.csv"

HEADER = "timestamp,cpu_percent,rss_kb"
NUM_SAMPLES = 5
TOTAL_LINES = 1 + NUM_SAMPLES


def read_csv_lines():
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f]
        return lines
    except Exception as e:
        pytest.fail(f"Could not read {CSV_PATH}: {e}")


def test_csv_file_exists_and_readable():
    assert os.path.isfile(CSV_PATH), (
        f"File {CSV_PATH} does not exist. "
        "The profile_log.csv file must be created at the specified location."
    )
    assert os.access(CSV_PATH, os.R_OK), (
        f"File {CSV_PATH} is not readable. "
        "Ensure the file has correct permissions."
    )


def test_csv_line_count_and_no_trailing_lines():
    lines = read_csv_lines()
    assert len(lines) == TOTAL_LINES, (
        f"{CSV_PATH} must have exactly {TOTAL_LINES} lines (1 header + 5 samples), "
        f"but found {len(lines)}."
    )


def test_csv_header_exact():
    lines = read_csv_lines()
    assert lines[0] == HEADER, (
        f"First line of {CSV_PATH} must be exactly '{HEADER}', "
        f"but found: '{lines[0]}'."
    )


def _parse_sample_line(line):
    # Returns (timestamp:int, cpu:str, rss:str)
    parts = line.split(",")
    if len(parts) != 3:
        return None
    ts, cpu, rss = parts
    return ts, cpu, rss


def test_csv_sample_lines_format_and_consistency():
    lines = read_csv_lines()
    sample_lines = lines[1:]
    assert len(sample_lines) == NUM_SAMPLES, (
        f"{CSV_PATH} must have 5 data sample lines after the header."
    )

    prev_ts = None
    for idx, line in enumerate(sample_lines):
        parsed = _parse_sample_line(line)
        assert parsed is not None, (
            f"Line {idx+2} in {CSV_PATH} is not a valid CSV line with three fields: '{line}'"
        )
        ts, cpu, rss = parsed
        # Timestamp checks
        assert ts.isdigit(), (
            f"Timestamp field at line {idx+2} must be an integer UNIX epoch, got '{ts}'."
        )
        ts_int = int(ts)
        if prev_ts is not None:
            assert ts_int == prev_ts + 1, (
                f"Timestamps must increase by exactly 1 second per sample. "
                f"Line {idx+1}: {prev_ts}, Line {idx+2}: {ts_int}."
            )
        prev_ts = ts_int

        # Data fields
        if cpu == "ERROR" and rss == "ERROR":
            continue  # Acceptable error row
        # Otherwise, both must be valid values
        assert cpu != "ERROR" and rss != "ERROR", (
            f"If the process is missing, both cpu_percent and rss_kb must be 'ERROR'. "
            f"Line {idx+2} has mixed/invalid values: '{line}'."
        )
        # cpu must be a float with exactly one decimal
        assert re.fullmatch(r"\d+\.\d", cpu), (
            f"cpu_percent value at line {idx+2} must be a float with exactly one digit after the decimal, got '{cpu}'."
        )
        # rss must be an integer
        assert rss.isdigit(), (
            f"rss_kb value at line {idx+2} must be a whole number (integer), got '{rss}'."
        )


def test_csv_no_extra_lines():
    # No empty lines or footers
    with open(CSV_PATH, "rb") as f:
        content = f.read()
    # File must end with the last sample, not an extra newline
    if content.endswith(b"\n"):
        # If file ends with newline, check for double newline at end
        assert not content.endswith(b"\n\n"), (
            f"{CSV_PATH} must not have extra blank lines at the end."
        )