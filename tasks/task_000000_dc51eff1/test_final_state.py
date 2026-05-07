# test_final_state.py

import os
import pytest

AUDIT_CONFIGS_DIR = "/home/user/audit_configs"
SERVER_YAML = "/home/user/audit_configs/server.yaml"
SECURITY_TOML = "/home/user/audit_configs/security.toml"
MAX_CONNECTIONS_REPORT = "/home/user/audit_configs/max_connections_report.txt"

EXPECTED_SERVER_YAML_CONTENT = (
    "---\n"
    "port: 8080\n"
    'host: "127.0.0.1"\n'
    "max_connections: 250\n"
    "debug: false\n"
)

EXPECTED_SECURITY_TOML_CONTENT = (
    "[settings]\n"
    "encryption = true\n"
    'firewall = "enabled"\n'
    "max_connections = 150\n"
)

EXPECTED_MAX_CONNECTIONS_REPORT = (
    "Server YAML max_connections: 250\n"
    "Security TOML max_connections: 150\n"
)

@pytest.mark.describe("Final filesystem state after audit configuration extraction task")
class TestFinalState:
    def test_audit_configs_directory_exists(self):
        assert os.path.isdir(AUDIT_CONFIGS_DIR), (
            f"Directory '{AUDIT_CONFIGS_DIR}' is missing after task completion. "
            "It must still exist."
        )

    def test_server_yaml_exists_and_unchanged(self):
        assert os.path.isfile(SERVER_YAML), (
            f"File '{SERVER_YAML}' is missing after task completion. "
            "It must not be deleted."
        )
        with open(SERVER_YAML, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == EXPECTED_SERVER_YAML_CONTENT, (
            f"File '{SERVER_YAML}' was modified. "
            "Its content must remain exactly:\n"
            f"{EXPECTED_SERVER_YAML_CONTENT}"
        )

    def test_security_toml_exists_and_unchanged(self):
        assert os.path.isfile(SECURITY_TOML), (
            f"File '{SECURITY_TOML}' is missing after task completion. "
            "It must not be deleted."
        )
        with open(SECURITY_TOML, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == EXPECTED_SECURITY_TOML_CONTENT, (
            f"File '{SECURITY_TOML}' was modified. "
            "Its content must remain exactly:\n"
            f"{EXPECTED_SECURITY_TOML_CONTENT}"
        )

    def test_max_connections_report_exists(self):
        assert os.path.isfile(MAX_CONNECTIONS_REPORT), (
            f"File '{MAX_CONNECTIONS_REPORT}' does not exist. "
            "You must create this file as the output of the task."
        )

    def test_max_connections_report_content(self):
        assert os.path.isfile(MAX_CONNECTIONS_REPORT), (
            f"File '{MAX_CONNECTIONS_REPORT}' does not exist. "
            "You must create this file as the output of the task."
        )
        with open(MAX_CONNECTIONS_REPORT, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == EXPECTED_MAX_CONNECTIONS_REPORT, (
            f"File '{MAX_CONNECTIONS_REPORT}' does not have the correct content.\n"
            "It must match exactly:\n"
            f"{EXPECTED_MAX_CONNECTIONS_REPORT}"
            f"Current content is:\n{content}"
        )

    def test_audit_configs_permissions(self):
        assert os.access(AUDIT_CONFIGS_DIR, os.W_OK), (
            f"No write access to directory '{AUDIT_CONFIGS_DIR}' after task completion. "
            "You must retain write access."
        )
        for file_path in [SERVER_YAML, SECURITY_TOML, MAX_CONNECTIONS_REPORT]:
            assert os.access(file_path, os.W_OK), (
                f"No write access to file '{file_path}' after task completion. "
                "You must retain write access."
            )