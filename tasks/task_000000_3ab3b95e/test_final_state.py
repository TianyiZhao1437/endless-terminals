# test_final_state.py
"""
Pytest suite to validate the FINAL OS/filesystem state for the network diagnostics task.

This test verifies that the log file "/home/user/network_investigation.log" exists and STRICTLY matches
the expected content, including section headers, bullet formatting, diagnostic values, summaries,
and order, as specified in the ground-truth for automated grading.

Failures will report exactly what is still wrong with the log file.
"""

import os
import pytest

LOG_PATH = "/home/user/network_investigation.log"

# The expected log content, as a single string (with trailing newline)
EXPECTED_LOG = (
"""===== DNS RESOLUTION =====
- example.com resolves to: 93.184.216.34
Summary: DNS resolution successful, IP address obtained.

===== ICMP PING =====
- example.com reachable: Yes
- Packet loss: 0%
- Average latency: 25.5 ms
Summary: Host is reachable with low latency and no packet loss.

===== TCP PORT SCAN =====
- Port 22: Closed
- Port 80: Open
- Port 443: Open
Summary: Ports 80 and 443 are accessible, port 22 is not.

===== TRACEROUTE =====
- Hop 1: 192.168.1.1
- Hop 2: 10.0.0.1
- Hop 3: 172.16.0.1
- Hop 4: 203.0.113.1
- Hop 5: 93.184.216.34
Total hops: 5
Summary: Traceroute completed in 5 hops.

===== LOCAL NETWORK CONFIGURATION =====
- Primary interface: eth0
- IPv4 address: 192.168.1.100
- Default gateway: 192.168.1.1
Summary: System uses eth0 with IP 192.168.1.100, gateway 192.168.1.1.
"""
)

def test_log_file_exists():
    """
    The log file /home/user/network_investigation.log must exist after task completion.
    """
    assert os.path.isfile(LOG_PATH), (
        f"Log file '{LOG_PATH}' does not exist. "
        "You must create this file with the required diagnostics."
    )

def test_log_file_content_exact():
    """
    The log file must match the expected content EXACTLY, including headers, order, values,
    bullet formatting, spacing, and summaries.
    """
    if not os.path.isfile(LOG_PATH):
        pytest.skip(f"Log file {LOG_PATH} missing, skipping content check.")

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        actual = f.read()

    if actual != EXPECTED_LOG:
        # Find and report the first difference
        import difflib
        diff = list(difflib.unified_diff(
            EXPECTED_LOG.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        ))
        max_lines = 20
        diff_str = "".join(diff[:max_lines])
        if len(diff) > max_lines:
            diff_str += f"\n... (diff truncated, file differs beyond {max_lines} lines)\n"
        assert False, (
            "Log file content does NOT match the required format or values.\n"
            "First differences (unified diff):\n"
            f"{diff_str}\n"
            "Check section headers, bullet formatting, values, summaries, and order."
        )

def test_log_file_no_extra_content():
    """
    The log file should not have extra content (e.g., trailing lines, extra whitespace).
    """
    with open(LOG_PATH, "rb") as f:
        raw = f.read()
    # Ensure no extra blank lines or bytes after the expected content
    expected_bytes = EXPECTED_LOG.encode("utf-8")
    assert raw == expected_bytes, (
        "Log file contains extra content or whitespace at the end. "
        "It must end exactly as specified."
    )