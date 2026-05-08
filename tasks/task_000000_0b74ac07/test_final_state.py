"""
test_final_state.py

Pytest suite to validate the FINAL state of the operating-system / container after the
technical writer workspace setup task has been completed.

Task truth:
- Directory: /home/user/docs_project
- File: /home/user/docs_project/README.txt
  Contents (exactly, including line breaks):
    Project: Linux Documentation
    Author: Alex Doe
    Version: 1.0
- File: /home/user/docs_project/env_config.log
  Contents (exactly, one line):
    /home/user/docs_project/README.txt
"""

import os
import pytest

DOCS_DIR = "/home/user/docs_project"
README_PATH = "/home/user/docs_project/README.txt"
ENV_CONFIG_PATH = "/home/user/docs_project/env_config.log"

README_EXPECTED_CONTENT = (
    "Project: Linux Documentation\n"
    "Author: Alex Doe\n"
    "Version: 1.0\n"
)

ENV_CONFIG_EXPECTED_CONTENT = f"{README_PATH}\n"

def test_docs_project_directory_final_state():
    assert os.path.isdir(DOCS_DIR), (
        f"Final state error: Directory missing at {DOCS_DIR}. "
        "You must ensure this directory exists after completing the task."
    )

def test_docs_project_directory_is_not_empty():
    contents = os.listdir(DOCS_DIR)
    expected = {"README.txt", "env_config.log"}
    missing = expected - set(contents)
    unexpected = set(contents) - expected
    assert not missing, (
        f"Final state error: The following files are missing in {DOCS_DIR}: {sorted(missing)}"
    )
    assert not unexpected, (
        f"Final state error: Unexpected files found in {DOCS_DIR}: {sorted(unexpected)}"
    )

def test_readme_txt_exists_final_state():
    assert os.path.isfile(README_PATH), (
        f"Final state error: README.txt missing at {README_PATH}. "
        "You must create this file inside /home/user/docs_project."
    )

def test_readme_txt_content_final_state():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == README_EXPECTED_CONTENT, (
        "Final state error: README.txt contents are incorrect.\n"
        "Expected exactly:\n"
        f"{README_EXPECTED_CONTENT!r}\n"
        "But found:\n"
        f"{content!r}\n"
        "Ensure the file contains exactly three lines, each with a key-value pair, and no extra or missing lines/characters."
    )

def test_env_config_log_exists_final_state():
    assert os.path.isfile(ENV_CONFIG_PATH), (
        f"Final state error: env_config.log missing at {ENV_CONFIG_PATH}. "
        "You must create this file inside /home/user/docs_project."
    )

def test_env_config_log_content_final_state():
    with open(ENV_CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == ENV_CONFIG_EXPECTED_CONTENT, (
        "Final state error: env_config.log contents are incorrect.\n"
        "Expected exactly:\n"
        f"{ENV_CONFIG_EXPECTED_CONTENT!r}\n"
        "But found:\n"
        f"{content!r}\n"
        "Ensure the file contains only the absolute path to README.txt, on a single line, with no extra lines or information."
    )