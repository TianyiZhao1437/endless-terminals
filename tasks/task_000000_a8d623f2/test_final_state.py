# test_final_state.py

import os
import stat
import pytest

ARTIFACTS_DIR = "/home/user/mlops/artifacts/"
LOGS_DIR = "/home/user/mlops/artifacts/logs/"
SECURITY_REPORT = "/home/user/mlops/security_fix_report.txt"

EXPERIMENT1_LOG = "/home/user/mlops/artifacts/logs/experiment1.log"
EXPERIMENT2_LOG = "/home/user/mlops/artifacts/logs/experiment2.log"
EXPERIMENT3_LOG = "/home/user/mlops/artifacts/logs/experiment3.log"

def read_file_lines(path):
    with open(path, "r") as f:
        return [line.rstrip('\n') for line in f]

def test_artifacts_dir_permissions():
    assert os.path.isdir(ARTIFACTS_DIR), f"Directory missing: {ARTIFACTS_DIR}"
    st = os.stat(ARTIFACTS_DIR)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o755, (
        f"Permissions for {ARTIFACTS_DIR} should be 755 (drwxr-xr-x), "
        f"but found {oct(mode)}"
    )

@pytest.mark.parametrize("log_path,expected_lines", [
    (EXPERIMENT1_LOG, [
        "Run 2024-01-02 13:43:12 completed.",
        "Accuracy: 0.912",
    ]),
    (EXPERIMENT2_LOG, [
        "Run 2024-01-02 14:15:28 completed.",
        "Loss: 0.043",
    ]),
    (EXPERIMENT3_LOG, [
        "Run 2024-01-02 15:20:12 completed.",
        "Accuracy: 0.887",
        "Notes: learning rate changed.",
    ]),
])
def test_log_file_contents(log_path, expected_lines):
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"
    lines = read_file_lines(log_path)
    assert lines == expected_lines, (
        f"Log file {log_path} does not match expected contents after secrets removal.\n"
        f"Expected:\n{expected_lines}\nActual:\n{lines}"
    )

def test_no_secrets_left_in_logs():
    # Ensure no log file has API_KEY= or SECRET= lines
    for log_path in [EXPERIMENT1_LOG, EXPERIMENT2_LOG, EXPERIMENT3_LOG]:
        with open(log_path, "r") as f:
            for lineno, line in enumerate(f, 1):
                assert "API_KEY=" not in line, (
                    f"Found API_KEY secret in {log_path} on line {lineno} after cleanup: {line.rstrip()}"
                )
                assert "SECRET=" not in line, (
                    f"Found SECRET secret in {log_path} on line {lineno} after cleanup: {line.rstrip()}"
                )

def test_security_fix_report_exists():
    assert os.path.isfile(SECURITY_REPORT), (
        f"Security report file does not exist: {SECURITY_REPORT}"
    )

def test_security_fix_report_contents():
    expected_report = (
        "[Permissions]\n"
        "Changed permissions: /home/user/mlops/artifacts/ to 755\n"
        "\n"
        "[Secrets Removed]\n"
        "/home/user/mlops/artifacts/logs/experiment1.log:\n"
        "  Removed line: API_KEY=abc123\n"
        "  Removed line: SECRET=supersecret\n"
        "\n"
        "/home/user/mlops/artifacts/logs/experiment2.log:\n"
        "  Removed line: API_KEY=xyz789\n"
    )
    with open(SECURITY_REPORT, "r") as f:
        actual_report = f.read()
    assert actual_report == expected_report, (
        f"{SECURITY_REPORT} does not exactly match the expected format and contents.\n"
        f"Expected:\n{expected_report!r}\nActual:\n{actual_report!r}"
    )