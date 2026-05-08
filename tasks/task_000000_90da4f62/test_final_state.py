# test_final_state.py

import os
import pytest

CERT_LOG_PATH = "/home/user/cert_expiry_audit.log"
EXPECTED_CERT_DATE = "Apr 24 12:00:00 2026 GMT"

@pytest.mark.describe("Final system state after cert audit task")
class TestFinalState:
    def test_cert_expiry_audit_log_exists(self):
        """The log file must exist after the task is completed."""
        assert os.path.exists(CERT_LOG_PATH), (
            f"The file {CERT_LOG_PATH} does not exist. "
            "You must create this file with the certificate NotAfter date."
        )

    def test_cert_expiry_audit_log_content_exact(self):
        """
        The log file must contain ONLY the exact NotAfter date from example.com's certificate,
        in the format: 'Apr 24 12:00:00 2026 GMT'
        """
        with open(CERT_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 1, (
            f"The file {CERT_LOG_PATH} must contain exactly one line. "
            f"Found {len(lines)} lines."
        )

        line = lines[0].rstrip("\n")

        assert line == EXPECTED_CERT_DATE, (
            f"The file {CERT_LOG_PATH} does not contain the correct NotAfter date.\n"
            f"Expected: '{EXPECTED_CERT_DATE}'\nFound:    '{line}'"
        )

    def test_cert_expiry_audit_log_no_extra_whitespace(self):
        """The log file must not contain extra whitespace, blank lines, or trailing spaces."""
        with open(CERT_LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for trailing whitespace or blank lines
        assert content == EXPECTED_CERT_DATE + "\n", (
            f"The file {CERT_LOG_PATH} must contain only the NotAfter date followed by a single newline.\n"
            f"Actual file content (repr): {repr(content)}"
        )