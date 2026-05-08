# test_final_state.py

import os
import pytest

PROM_DASHBOARD_JSON = "/home/user/prometheus_dashboard.json"
GRAFANA_DASHBOARD_JSON = "/home/user/grafana/provisioning/dashboards/prometheus_dashboard.json"
COPY_DASHBOARD_LOG = "/home/user/copy_dashboard.log"

EXPECTED_LOG_LINE = (
    "SUCCESS: /home/user/prometheus_dashboard.json -> "
    "/home/user/grafana/provisioning/dashboards/prometheus_dashboard.json"
)

@pytest.mark.describe("Final OS/filesystem state validation after copying dashboard JSON")
def test_grafana_dashboard_json_exists_and_is_identical():
    """
    Ensure the copied dashboard JSON exists at the target location and is byte-for-byte identical
    to the original /home/user/prometheus_dashboard.json.
    """
    # Check existence
    assert os.path.isfile(GRAFANA_DASHBOARD_JSON), (
        f"File '{GRAFANA_DASHBOARD_JSON}' does not exist. "
        "You must copy the dashboard JSON to the Grafana provisioning directory."
    )
    assert os.path.isfile(PROM_DASHBOARD_JSON), (
        f"Source file '{PROM_DASHBOARD_JSON}' does not exist. "
        "The source dashboard JSON must remain present after the task."
    )
    # Check content
    with open(PROM_DASHBOARD_JSON, "rb") as f_src, open(GRAFANA_DASHBOARD_JSON, "rb") as f_dst:
        src_bytes = f_src.read()
        dst_bytes = f_dst.read()
    assert src_bytes == dst_bytes, (
        f"File '{GRAFANA_DASHBOARD_JSON}' does not exactly match '{PROM_DASHBOARD_JSON}'. "
        "The copy must be byte-for-byte identical. Check for formatting, whitespace, or copy errors."
    )

def test_copy_dashboard_log_exists_and_correct():
    """
    Ensure the log file /home/user/copy_dashboard.log exists and contains exactly the required line,
    with no extra whitespace, lines, or deviations.
    """
    assert os.path.isfile(COPY_DASHBOARD_LOG), (
        f"Log file '{COPY_DASHBOARD_LOG}' does not exist. "
        "You must create this log file after copying the dashboard JSON."
    )
    with open(COPY_DASHBOARD_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check for exactly one line
    assert len(lines) == 1, (
        f"Log file '{COPY_DASHBOARD_LOG}' must contain exactly one line. "
        f"Found {len(lines)} lines. Check for extra lines or blank lines."
    )
    # Strip trailing newline for comparison
    log_line = lines[0].rstrip('\n')
    assert log_line == EXPECTED_LOG_LINE, (
        f"Log file '{COPY_DASHBOARD_LOG}' does not contain the required success line.\n"
        f"Expected:\n{EXPECTED_LOG_LINE!r}\nFound:\n{log_line!r}\n"
        "Check for extra whitespace, missing text, or formatting errors."
    )