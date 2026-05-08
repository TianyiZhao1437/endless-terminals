# test_initial_state.py

import os
import pytest

CLOUD_COSTS_DIR = "/home/user/cloud_costs"
MONTHLY_REPORT_PATH = os.path.join(CLOUD_COSTS_DIR, "monthly_report.csv")

MONTHLY_REPORT_EXPECTED = """date,project,service,cost
2024-06-01,analytics,compute,24.56
2024-06-02,storage,storage,31.22
2024-06-03,analytics,compute,35.44
2024-06-04,web,cdn,12.10
2024-06-05,storage,backup,29.99
2024-06-06,analytics,compute,40.08
"""

TOTAL_SPEND_PATH = os.path.join(CLOUD_COSTS_DIR, "total_spend.txt")
HIGH_USAGE_PATH = os.path.join(CLOUD_COSTS_DIR, "high_usage.csv")

@pytest.mark.parametrize(
    "path", [
        (CLOUD_COSTS_DIR),
        (MONTHLY_REPORT_PATH)
    ]
)
def test_preexisting_files_and_dirs(path):
    if path == CLOUD_COSTS_DIR:
        assert os.path.isdir(path), (
            f"Required directory does not exist: {path}"
        )
    else:
        assert os.path.isfile(path), (
            f"Required file does not exist: {path}"
        )

def test_monthly_report_csv_contents():
    assert os.path.isfile(MONTHLY_REPORT_PATH), (
        f"monthly_report.csv is missing at {MONTHLY_REPORT_PATH}"
    )
    with open(MONTHLY_REPORT_PATH, "r", encoding="utf-8") as f:
        contents = f.read()
    # Normalize line endings for robust comparison
    actual = contents.replace('\r\n', '\n').strip()
    expected = MONTHLY_REPORT_EXPECTED.strip()
    assert actual == expected, (
        f"monthly_report.csv does not have the expected contents.\n"
        f"Expected:\n{expected}\n\nActual:\n{actual}"
    )

def test_output_files_do_not_exist_yet():
    """
    The output files must NOT exist before the student performs the task.
    """
    for path in [TOTAL_SPEND_PATH, HIGH_USAGE_PATH]:
        assert not os.path.exists(path), (
            f"Output file should not exist yet: {path}"
        )