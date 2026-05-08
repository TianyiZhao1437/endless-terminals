# test_final_state.py

import os
import pytest

CSV_PATH = "/home/user/server_resources.csv"
JSON_PATH = "/home/user/resource_summary.json"
HOME_PATH = "/home/user"

EXPECTED_CSV = (
    "server_id,cpu_usage,memory_usage\n"
    "svr01,80.1,4094\n"
    "svr01,76.4,4097\n"
    "svr02,65.0,2048.35\n"
)

EXPECTED_JSON = (
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


@pytest.mark.describe("Final OS/filesystem state after capacity planner resource summary task")
class TestFinalState:

    def test_home_directory_exists_and_writable(self):
        assert os.path.isdir(HOME_PATH), (
            f"Required home directory {HOME_PATH} does not exist."
        )
        assert os.access(HOME_PATH, os.W_OK), (
            f"Home directory {HOME_PATH} is not writable by the user."
        )

    def test_server_resources_csv_exists_and_unchanged(self):
        assert os.path.isfile(CSV_PATH), (
            f"CSV file {CSV_PATH} is missing after task completion."
        )
        assert os.access(CSV_PATH, os.R_OK | os.W_OK), (
            f"CSV file {CSV_PATH} is not readable and writable by the user."
        )
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == EXPECTED_CSV, (
            f"CSV file {CSV_PATH} was modified during the task.\n"
            "Expected:\n"
            f"{EXPECTED_CSV}\n"
            "Actual:\n"
            f"{actual}"
        )

    def test_resource_summary_json_exists_and_correct(self):
        assert os.path.isfile(JSON_PATH), (
            f"JSON summary file {JSON_PATH} does not exist."
        )
        assert os.access(JSON_PATH, os.R_OK | os.W_OK), (
            f"JSON summary file {JSON_PATH} is not readable and writable by the user."
        )
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == EXPECTED_JSON, (
            f"JSON summary file {JSON_PATH} does not match the required format and contents.\n"
            "Expected:\n"
            f"{EXPECTED_JSON}\n"
            "Actual:\n"
            f"{actual}"
            "\n"
            "Ensure the output is:\n"
            "- A dictionary mapping each server_id to an object with avg_cpu_usage and avg_memory_usage\n"
            "- All numeric values rounded to two decimal places\n"
            "- Indented with exactly 2 spaces per level\n"
            "- In the same order and with the same formatting as shown above\n"
        )