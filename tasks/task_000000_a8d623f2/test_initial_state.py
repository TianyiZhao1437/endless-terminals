# test_initial_state.py
import os
import pytest

ARTIFACTS_DIR = "/home/user/mlops/artifacts/"
LOGS_DIR = "/home/user/mlops/artifacts/logs/"
SECURITY_REPORT = "/home/user/mlops/security_fix_report.txt"

EXPERIMENT1_LOG = "/home/user/mlops/artifacts/logs/experiment1.log"
EXPERIMENT2_LOG = "/home/user/mlops/artifacts/logs/experiment2.log"
EXPERIMENT3_LOG = "/home/user/mlops/artifacts/logs/experiment3.log"

@pytest.mark.parametrize("path", [
    ARTIFACTS_DIR,
    LOGS_DIR,
    EXPERIMENT1_LOG,
    EXPERIMENT2_LOG,
    EXPERIMENT3_LOG,
])
def test_required_paths_exist(path):
    assert os.path.exists(path), f"Required path does not exist: {path}"

def test_artifacts_dir_world_writable():
    st = os.stat(ARTIFACTS_DIR)
    mode = st.st_mode & 0o777
    assert mode == 0o777, (
        f"Directory {ARTIFACTS_DIR} should be world-writable (mode 777) before any changes, "
        f"but found mode {oct(mode)}"
    )

def test_logs_dir_is_directory():
    assert os.path.isdir(LOGS_DIR), f"{LOGS_DIR} should be a directory"

@pytest.mark.parametrize("log_path,expected_lines", [
    (EXPERIMENT1_LOG, [
        "Run 2024-01-02 13:43:12 completed.",
        "Accuracy: 0.912",
        "API_KEY=abc123",
        "SECRET=supersecret",
    ]),
    (EXPERIMENT2_LOG, [
        "Run 2024-01-02 14:15:28 completed.",
        "Loss: 0.043",
        "API_KEY=xyz789",
    ]),
    (EXPERIMENT3_LOG, [
        "Run 2024-01-02 15:20:12 completed.",
        "Accuracy: 0.887",
        "Notes: learning rate changed.",
    ]),
])
def test_log_file_contents(log_path, expected_lines):
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == expected_lines, (
        f"Log file {log_path} does not match expected initial contents.\n"
        f"Expected:\n{expected_lines}\nActual:\n{lines}"
    )

def test_security_report_does_not_exist():
    assert not os.path.exists(SECURITY_REPORT), (
        f"{SECURITY_REPORT} should not exist before the student performs any actions."
    )