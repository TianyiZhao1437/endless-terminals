# test_initial_state.py

import os
import pytest

CSV_PATH = "/home/user/server_resources.csv"
JSON_PATH = "/home/user/resource_summary.json"
HOME_PATH = "/home/user"

@pytest.mark.describe("Initial OS/filesystem state for capacity planner task")
class TestInitialState:

    def test_home_directory_exists_and_writable(self):
        assert os.path.isdir(HOME_PATH), (
            f"Required home directory {HOME_PATH} does not exist."
        )
        assert os.access(HOME_PATH, os.W_OK), (
            f"Home directory {HOME_PATH} is not writable by the user."
        )

    def test_server_resources_csv_exists_and_readable(self):
        assert os.path.isfile(CSV_PATH), (
            f"Required CSV file {CSV_PATH} does not exist."
        )
        assert os.access(CSV_PATH, os.R_OK | os.W_OK), (
            f"CSV file {CSV_PATH} is not readable and writable by the user."
        )

    def test_server_resources_csv_contents(self):
        expected = (
            "server_id,cpu_usage,memory_usage\n"
            "svr01,80.1,4094\n"
            "svr01,76.4,4097\n"
            "svr02,65.0,2048.35\n"
        )
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == expected, (
            f"CSV file {CSV_PATH} does not have the expected contents.\n"
            "Expected:\n"
            f"{expected}\n"
            "Actual:\n"
            f"{actual}"
        )

    def test_resource_summary_json_exists_and_readable(self):
        assert os.path.isfile(JSON_PATH), (
            f"Required JSON file {JSON_PATH} does not exist."
        )
        assert os.access(JSON_PATH, os.R_OK | os.W_OK), (
            f"JSON file {JSON_PATH} is not readable and writable by the user."
        )

    def test_resource_summary_json_contents(self):
        expected = (
            '{\n'
            '  "svr01": {\n'
            '    "avg_cpu_usage": 78.25,\n'
            '    "avg_memory_usage": 4095.50\n'
            '  },\n'
            '  "svr02": {\n'
            '    "avg_cpu_usage": 65.00,\n'
            '    "avg_memory_usage": 2048.35\n'
            '  }\n'
            '}\n'
        )
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == expected, (
            f"JSON file {JSON_PATH} does not have the expected contents.\n"
            "Expected:\n"
            f"{expected}\n"
            "Actual:\n"
            f"{actual}"
        )