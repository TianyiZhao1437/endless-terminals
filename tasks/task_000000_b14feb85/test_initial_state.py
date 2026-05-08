# test_initial_state.py

import os
import configparser
import pytest

INI_PATH = "/home/user/cicd/configs/pipeline.ini"
AUDIT_DIR = "/home/user/cicd/audit"
AUDIT_LOG = "/home/user/cicd/audit/pipeline_audit.log"

@pytest.mark.describe("Initial OS/filesystem state for CI/CD pipeline audit automation task")
class TestInitialState:
    def test_pipeline_ini_exists(self):
        assert os.path.isfile(INI_PATH), (
            f"Missing required INI configuration file at: {INI_PATH}. "
            "This file is required to parse pipeline configuration."
        )

    def test_pipeline_ini_content_and_sections(self):
        assert os.path.isfile(INI_PATH), (
            f"INI file does not exist at {INI_PATH} to check content."
        )
        config = configparser.ConfigParser()
        config.optionxform = str  # case-sensitive keys
        with open(INI_PATH, "r") as f:
            config.read_file(f)
        required_sections = ["git", "docker", "notifications"]
        for section in required_sections:
            assert section in config, (
                f"Missing required section [{section}] in {INI_PATH}."
            )

    def test_pipeline_ini_git_section_keys(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # case-sensitive keys
        with open(INI_PATH, "r") as f:
            config.read_file(f)
        required_keys = ["url", "branch", "shallow_clone"]
        for key in required_keys:
            assert key in config["git"], (
                f"Missing key '{key}' in [git] section of {INI_PATH}."
            )

    def test_pipeline_ini_docker_section_keys(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # case-sensitive keys
        with open(INI_PATH, "r") as f:
            config.read_file(f)
        required_keys = ["image", "tag", "build_args"]
        for key in required_keys:
            assert key in config["docker"], (
                f"Missing key '{key}' in [docker] section of {INI_PATH}."
            )

    def test_pipeline_ini_notifications_section_keys(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # case-sensitive keys
        with open(INI_PATH, "r") as f:
            config.read_file(f)
        required_keys = ["email_on_failure", "slack_webhook"]
        for key in required_keys:
            assert key in config["notifications"], (
                f"Missing key '{key}' in [notifications] section of {INI_PATH}."
            )

    def test_audit_directory_does_not_exist(self):
        assert not os.path.exists(AUDIT_DIR), (
            f"The audit directory {AUDIT_DIR} already exists, "
            "but it should NOT be present before the pipeline audit task begins."
        )

    def test_audit_log_does_not_exist(self):
        assert not os.path.exists(AUDIT_LOG), (
            f"The audit log file {AUDIT_LOG} already exists, "
            "but it should NOT be present before the pipeline audit task begins."
        )