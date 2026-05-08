# test_initial_state.py

import os
import pytest
import shutil
import socket
import ssl
import datetime

CERT_LOG_PATH = "/home/user/cert_expiry_audit.log"
EXAMPLE_COM = "example.com"
EXAMPLE_COM_PORT = 443

@pytest.mark.describe("Initial system state before cert audit")
class TestInitialState:
    def test_cert_expiry_audit_log_does_not_exist(self):
        """The log file should NOT exist before the user runs the task."""
        assert not os.path.exists(CERT_LOG_PATH), (
            f"The file {CERT_LOG_PATH} already exists. "
            f"Please remove it before starting the task."
        )

    def test_openssl_binary_exists(self):
        """openssl binary must be available for the student to use."""
        openssl_path = shutil.which("openssl")
        assert openssl_path is not None, (
            "The 'openssl' binary is not found in the PATH. "
            "Please ensure OpenSSL is installed and available."
        )

    def test_can_connect_to_example_com_on_443(self):
        """Ensure example.com:443 is reachable for SSL connection."""
        try:
            with socket.create_connection((EXAMPLE_COM, EXAMPLE_COM_PORT), timeout=10) as sock:
                pass
        except Exception as e:
            pytest.fail(
                f"Could not connect to {EXAMPLE_COM}:443. "
                f"Check your network connection. Exception: {e}"
            )

    def test_can_retrieve_certificate_and_notafter(self):
        """Ensure the NotAfter date can be retrieved from example.com via SSL."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((EXAMPLE_COM, EXAMPLE_COM_PORT), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=EXAMPLE_COM) as ssock:
                    cert = ssock.getpeercert()
        except Exception as e:
            pytest.fail(
                f"Failed to retrieve SSL certificate from {EXAMPLE_COM}:443. "
                f"Exception: {e}"
            )
        not_after = cert.get("notAfter")
        assert not_after is not None, (
            "Could not extract 'notAfter' field from example.com's certificate. "
            "Certificate fields: {}".format(cert)
        )
        # Check format: e.g., 'Apr 24 12:00:00 2026 GMT'
        try:
            datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        except Exception:
            pytest.fail(
                f"'notAfter' field of example.com's certificate is not in the expected OpenSSL format: "
                f"'Apr 24 12:00:00 2026 GMT'. Got: '{not_after}'"
            )