# test_initial_state.py

import os
import pytest

AUDIT_CONFIGS_DIR = "/home/user/audit_configs"
SERVER_YAML = "/home/user/audit_configs/server.yaml"
SECURITY_TOML = "/home/user/audit_configs/security.toml"
MAX_CONNECTIONS_REPORT = "/home/user/audit_configs/max_connections_report.txt"

@pytest.mark.describe("Initial filesystem state for audit configuration extraction task")
class TestInitialState:
    def test_audit_configs_directory_exists(self):
        assert os.path.isdir(AUDIT_CONFIGS_DIR), (
            f"Required directory '{AUDIT_CONFIGS_DIR}' does not exist. "
            "Ensure the directory is present before starting the task."
        )

    def test_server_yaml_exists(self):
        assert os.path.isfile(SERVER_YAML), (
            f"Required file '{SERVER_YAML}' does not exist. "
            "Create this file with the correct server configuration before starting the task."
        )

    def test_security_toml_exists(self):
        assert os.path.isfile(SECURITY_TOML), (
            f"Required file '{SECURITY_TOML}' does not exist. "
            "Create this file with the correct security configuration before starting the task."
        )

    def test_max_connections_report_does_not_exist(self):
        assert not os.path.exists(MAX_CONNECTIONS_REPORT), (
            f"Output file '{MAX_CONNECTIONS_REPORT}' already exists. "
            "This file should not be present before the task begins."
        )

    def test_server_yaml_content(self):
        expected = (
            "---\n"
            "port: 8080\n"
            'host: "127.0.0.1"\n'
            "max_connections: 250\n"
            "debug: false\n"
        )
        with open(SERVER_YAML, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == expected, (
            f"File '{SERVER_YAML}' does not have the expected content. "
            "Ensure it matches exactly:\n"
            f"{expected}"
        )

    def test_security_toml_content(self):
        expected = (
            "[settings]\n"
            "encryption = true\n"
            'firewall = "enabled"\n'
            "max_connections = 150\n"
        )
        with open(SECURITY_TOML, "r", encoding="utf-8") as f:
            actual = f.read()
        assert actual == expected, (
            f"File '{SECURITY_TOML}' does not have the expected content. "
            "Ensure it matches exactly:\n"
            f"{expected}"
        )

    def test_audit_configs_permissions(self):
        # Check write access to directory and files
        assert os.access(AUDIT_CONFIGS_DIR, os.W_OK), (
            f"No write access to directory '{AUDIT_CONFIGS_DIR}'. "
            "Ensure you have permissions to write in this directory."
        )
        for file_path in [SERVER_YAML, SECURITY_TOML]:
            assert os.access(file_path, os.W_OK), (
                f"No write access to file '{file_path}'. "
                "Ensure you have permissions to edit this file if necessary."
            )