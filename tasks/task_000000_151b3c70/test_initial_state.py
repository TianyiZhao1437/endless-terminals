# test_initial_state.py

import os
import pytest

PROM_DASHBOARD_JSON = "/home/user/prometheus_dashboard.json"
GRAFANA_DASHBOARDS_DIR = "/home/user/grafana/provisioning/dashboards"

@pytest.mark.describe("Initial OS/filesystem state validation before copying dashboard JSON")
def test_prometheus_dashboard_json_exists_and_content():
    """
    Ensure the source Prometheus dashboard JSON file exists with the correct content.
    """
    assert os.path.isfile(PROM_DASHBOARD_JSON), (
        f"Required file '{PROM_DASHBOARD_JSON}' does not exist. "
        "You must have this file present before proceeding."
    )
    with open(PROM_DASHBOARD_JSON, "r", encoding="utf-8") as f:
        content = f.read()
    expected_content = '''{
  "dashboard": {
    "title": "Prometheus Metrics",
    "panels": [
      {
        "type": "graph",
        "title": "CPU Usage"
      }
    ]
  }
}
'''
    assert content == expected_content, (
        f"File '{PROM_DASHBOARD_JSON}' does not contain the expected content. "
        "Check that its contents exactly match the required JSON (including formatting and whitespace)."
    )

def test_grafana_dashboards_dir_exists():
    """
    Ensure the Grafana dashboards provisioning directory exists.
    """
    assert os.path.isdir(GRAFANA_DASHBOARDS_DIR), (
        f"Expected directory '{GRAFANA_DASHBOARDS_DIR}' does not exist. "
        "Make sure Grafana is set up and the provisioning dashboards directory is present before proceeding."
    )