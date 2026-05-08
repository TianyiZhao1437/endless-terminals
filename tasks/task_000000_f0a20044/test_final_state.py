# test_final_state.py

import os
import pytest

CLOUD_COSTS_DIR = "/home/user/cloud_costs"
MONTHLY_REPORT_PATH = os.path.join(CLOUD_COSTS_DIR, "monthly_report.csv")
TOTAL_SPEND_PATH = os.path.join(CLOUD_COSTS_DIR, "total_spend.txt")
HIGH_USAGE_PATH = os.path.join(CLOUD_COSTS_DIR, "high_usage.csv")

EXPECTED_TOTAL_SPEND = "Total Spend: 173.39"
EXPECTED_HIGH_USAGE = (
    "date,project,service,cost\n"
    "2024-06-02,storage,storage,31.22\n"
    "2024-06-03,analytics,compute,35.44\n"
    "2024-06-06,analytics,compute,40.08"
)

@pytest.mark.parametrize(
    "path", [
        (TOTAL_SPEND_PATH),
        (HIGH_USAGE_PATH),
    ]
)
def test_output_files_exist(path):
    assert os.path.isfile(path), (
        f"Required output file does not exist: {path}"
    )

def test_total_spend_txt_contents():
    """
    /home/user/cloud_costs/total_spend.txt must exist and contain exactly:
    Total Spend: 173.39
    (one line, no trailing/leading blank lines)
    """
    assert os.path.isfile(TOTAL_SPEND_PATH), (
        f"total_spend.txt is missing at {TOTAL_SPEND_PATH}"
    )
    with open(TOTAL_SPEND_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1, (
        f"total_spend.txt should contain exactly one line, found {len(lines)} lines."
    )

    content = lines[0].rstrip('\r\n')
    assert content == EXPECTED_TOTAL_SPEND, (
        f"total_spend.txt has incorrect contents.\n"
        f"Expected exactly:\n{EXPECTED_TOTAL_SPEND}\nActual:\n{content}"
    )

def test_high_usage_csv_contents():
    """
    /home/user/cloud_costs/high_usage.csv must exist and contain only:
    - The header row from monthly_report.csv
    - All rows where cost > 30.00 (as floats), in the same order as the source
    - CSV format preserved
    """
    assert os.path.isfile(HIGH_USAGE_PATH), (
        f"high_usage.csv is missing at {HIGH_USAGE_PATH}"
    )
    with open(HIGH_USAGE_PATH, "r", encoding="utf-8") as f:
        contents = f.read()

    # Normalize line endings for robust comparison
    actual = contents.replace('\r\n', '\n').strip()
    expected = EXPECTED_HIGH_USAGE.strip()
    assert actual == expected, (
        "high_usage.csv contents are incorrect.\n"
        f"Expected exactly:\n{expected}\n\nActual:\n{actual}"
    )

def test_no_extra_output_files():
    """
    There should be no extra files in /home/user/cloud_costs besides:
    - monthly_report.csv
    - total_spend.txt
    - high_usage.csv
    """
    expected_files = {
        "monthly_report.csv",
        "total_spend.txt",
        "high_usage.csv",
    }
    actual_files = set(os.listdir(CLOUD_COSTS_DIR))
    extra_files = actual_files - expected_files
    missing_files = expected_files - actual_files

    assert not missing_files, (
        f"Missing expected file(s) in {CLOUD_COSTS_DIR}: {', '.join(sorted(missing_files))}"
    )
    assert not extra_files, (
        f"Found unexpected file(s) in {CLOUD_COSTS_DIR}: {', '.join(sorted(extra_files))}"
    )