# test_final_state.py

import os
import pytest

LOG_FILE = "/home/user/etl_logs/pipeline_run.log"
EXPECTED_OUTPUT = [
    "payment_load",
    "product_transform",
    "sales_transform",
    "user_import"
]

def extract_failed_jobs_from_log(log_path):
    """
    Reads the log file and returns a sorted list of unique ETL job names that have failed.
    """
    failed_jobs = set()
    try:
        with open(log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Expected line format: [TIMESTAMP] ETL_JOB_NAME - STATUS
                try:
                    before_status, status = line.rsplit(" - ", 1)
                    _, jobname = before_status.split("] ", 1)
                    jobname = jobname.strip()
                    if status == "FAILED":
                        failed_jobs.add(jobname)
                except Exception as e:
                    # If parsing fails, that's a test failure
                    pytest.fail(
                        f"Malformed log line in '{log_path}': {line}\n"
                        f"Error: {e}\n"
                        "Each line must match: [TIMESTAMP] ETL_JOB_NAME - STATUS"
                    )
    except Exception as e:
        pytest.fail(f"Could not read log file '{log_path}': {e}")

    return sorted(failed_jobs)

def test_pipeline_run_log_failed_jobs_output():
    """
    Validates that the output of analyzing the log file matches the expected
    sorted, unique list of failed ETL job names.
    """
    assert os.path.isfile(LOG_FILE), (
        f"File '{LOG_FILE}' does not exist. "
        "Please ensure the log file pipeline_run.log is present in /home/user/etl_logs/."
    )

    failed_jobs = extract_failed_jobs_from_log(LOG_FILE)

    assert failed_jobs == EXPECTED_OUTPUT, (
        f"Incorrect failed ETL job output from log analysis.\n"
        f"Expected (one job per line, sorted, unique):\n"
        f"{chr(10).join(EXPECTED_OUTPUT)}\n"
        f"Actual:\n"
        f"{chr(10).join(failed_jobs)}\n"
        "Ensure your analysis outputs exactly the expected job names, sorted, one per line, with no duplicates."
    )