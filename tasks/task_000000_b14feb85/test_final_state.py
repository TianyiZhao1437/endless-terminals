# test_final_state.py

import os
import pytest

AUDIT_DIR = "/home/user/cicd/audit"
AUDIT_LOG = "/home/user/cicd/audit/pipeline_audit.log"
INI_PATH = "/home/user/cicd/configs/pipeline.ini"

EXPECTED_AUDIT_LOG = (
    "Git URL: https://github.com/example/project.git\n"
    "Git Branch: main\n"
    "Git Shallow Clone: true\n"
    "Docker Image: example/project\n"
    "Docker Tag: latest\n"
    "Docker Build Args: --no-cache\n"
    "Notifications Email On Failure: devops@example.com\n"
    "Notifications Slack Webhook: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX\n"
)

@pytest.mark.describe("Final OS/filesystem state after CI/CD pipeline audit automation task")
class TestFinalState:
    def test_audit_directory_created(self):
        assert os.path.isdir(AUDIT_DIR), (
            f"Audit directory {AUDIT_DIR} does not exist. "
            "The agent must create this directory before generating the audit log."
        )

    def test_audit_log_created(self):
        assert os.path.isfile(AUDIT_LOG), (
            f"Audit log file {AUDIT_LOG} does not exist. "
            "The agent must create this file containing the parsed pipeline summary."
        )

    def test_audit_log_content_exact(self):
        assert os.path.isfile(AUDIT_LOG), (
            f"Audit log file {AUDIT_LOG} does not exist to check content."
        )
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            actual_content = f.read()
        # Compare exact content, including newlines
        if actual_content != EXPECTED_AUDIT_LOG:
            # Find the first difference for easier debugging
            from difflib import unified_diff
            diff = "\n".join(unified_diff(
                EXPECTED_AUDIT_LOG.splitlines(keepends=True),
                actual_content.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual"
            ))
            pytest.fail(
                f"Audit log content is not exactly as required.\n"
                f"--- Diff between expected and actual below ---\n{diff}"
            )

    def test_ini_file_not_modified(self):
        # Ensure the original pipeline.ini is not altered
        expected_ini = (
            "[git]\n"
            "url = https://github.com/example/project.git\n"
            "branch = main\n"
            "shallow_clone = true\n"
            "\n"
            "[docker]\n"
            "image = example/project\n"
            "tag = latest\n"
            "build_args = --no-cache\n"
            "\n"
            "[notifications]\n"
            "email_on_failure = devops@example.com\n"
            "slack_webhook = https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX\n"
        )
        assert os.path.isfile(INI_PATH), (
            f"INI file missing at {INI_PATH} after task, but it must not be removed or moved."
        )
        with open(INI_PATH, "r", encoding="utf-8") as f:
            actual_ini = f.read()
        if actual_ini != expected_ini:
            from difflib import unified_diff
            diff = "\n".join(unified_diff(
                expected_ini.splitlines(keepends=True),
                actual_ini.splitlines(keepends=True),
                fromfile="expected_ini",
                tofile="actual_ini"
            ))
            pytest.fail(
                f"pipeline.ini content was modified during the audit, but it must remain unchanged!\n"
                f"--- Diff between expected and actual below ---\n{diff}"
            )