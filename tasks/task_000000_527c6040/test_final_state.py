# test_final_state.py
import os
import stat
import pytest

SCAN_SCRIPT_PATH = "/home/user/scan_targets.sh"
SCAN_LOG_PATH = "/home/user/scan_log.txt"
TARGETS_TXT_PATH = "/home/user/targets.txt"

EXPECTED_SCRIPT = '''#!/bin/bash
LOG="/home/user/scan_log.txt"
TARGETS="/home/user/targets.txt"
PORTS=(22 80 443)

> "$LOG"
while read -r target; do
    echo "Target: $target" >> "$LOG"
    for port in "${PORTS[@]}"; do
        if nc -z -w 1 "$target" "$port" 2>/dev/null; then
            status="open"
        else
            status="closed"
        fi
        echo "Port $port: $status" >> "$LOG"
    done
    echo "" >> "$LOG"
done < "$TARGETS"
'''.strip()

EXPECTED_LOG = (
    "Target: 192.168.0.10\n"
    "Port 22: open\n"
    "Port 80: closed\n"
    "Port 443: closed\n"
    "\n"
    "Target: 192.168.0.20\n"
    "Port 22: closed\n"
    "Port 80: open\n"
    "Port 443: open\n"
    "\n"
    "Target: test-host.local\n"
    "Port 22: closed\n"
    "Port 80: closed\n"
    "Port 443: closed\n"
)

def test_scan_script_exists():
    assert os.path.isfile(SCAN_SCRIPT_PATH), (
        f"Script file not found: {SCAN_SCRIPT_PATH}. "
        "You must create the shell script at this exact path."
    )

def test_scan_script_is_executable():
    st = os.stat(SCAN_SCRIPT_PATH)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, (
        f"The script {SCAN_SCRIPT_PATH} is not executable. "
        "Please ensure you 'chmod +x' the script."
    )

def test_scan_script_contents():
    with open(SCAN_SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
    # Normalize whitespace for comparison, but check for exact structure
    def norm(s):
        return "\n".join([line.rstrip() for line in s.strip().splitlines()])
    assert norm(content) == norm(EXPECTED_SCRIPT), (
        f"The script {SCAN_SCRIPT_PATH} does not match the expected contents.\n"
        "Expected script:\n"
        f"{EXPECTED_SCRIPT}\n"
        "Found script:\n"
        f"{content}"
    )

def test_scan_log_exists():
    assert os.path.isfile(SCAN_LOG_PATH), (
        f"Log file not found: {SCAN_LOG_PATH}. "
        "The log file must be created at this exact path."
    )

def test_scan_log_contents_exact():
    with open(SCAN_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for exact content, including blank lines, no trailing whitespace
    assert content == EXPECTED_LOG, (
        f"The log file {SCAN_LOG_PATH} does not have the correct contents.\n"
        "Expected:\n"
        f"{EXPECTED_LOG}\n"
        "Found:\n"
        f"{content}"
    )

def test_no_extra_files():
    files = set(os.listdir("/home/user"))
    expected_files = {"scan_targets.sh", "scan_log.txt", "targets.txt"}
    unexpected = files - expected_files
    assert not unexpected, (
        f"Unexpected files found in /home/user: {unexpected}. "
        "Only scan_targets.sh, scan_log.txt, and targets.txt should exist."
    )

def test_targets_txt_unchanged():
    expected_targets = [
        "192.168.0.10",
        "192.168.0.20",
        "test-host.local"
    ]
    with open(TARGETS_TXT_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f.readlines()]
    assert lines == expected_targets, (
        f"The file {TARGETS_TXT_PATH} has been modified.\n"
        f"Expected:\n" +
        "\n".join(expected_targets) +
        "\nFound:\n" +
        "\n".join(lines)
    )