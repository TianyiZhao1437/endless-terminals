# test_initial_state.py

import os
import pytest

DOCS_DIR = "/home/user/docs_project"
README_PATH = os.path.join(DOCS_DIR, "README.txt")
ENV_CONFIG_PATH = os.path.join(DOCS_DIR, "env_config.log")

README_EXPECTED_CONTENT = (
    "Project: Linux Documentation\n"
    "Author: Alex Doe\n"
    "Version: 1.0\n"
)

ENV_CONFIG_EXPECTED_CONTENT = f"{README_PATH}\n"

def test_docs_project_directory_exists():
    assert os.path.isdir(DOCS_DIR), (
        f"Missing directory: {DOCS_DIR}. "
        "You must create this directory before proceeding."
    )

def test_readme_txt_exists():
    assert os.path.isfile(README_PATH), (
        f"Missing file: {README_PATH}. "
        "You must create README.txt inside /home/user/docs_project."
    )

def test_readme_txt_content():
    assert os.path.isfile(README_PATH), (
        f"Missing file: {README_PATH}. "
        "You must create README.txt before checking its contents."
    )
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == README_EXPECTED_CONTENT, (
        f"README.txt contents are incorrect.\n"
        "Expected exactly:\n"
        f"{README_EXPECTED_CONTENT!r}\n"
        f"But found:\n"
        f"{content!r}"
    )

def test_env_config_log_exists():
    assert os.path.isfile(ENV_CONFIG_PATH), (
        f"Missing file: {ENV_CONFIG_PATH}. "
        "You must create env_config.log inside /home/user/docs_project."
    )

def test_env_config_log_content():
    assert os.path.isfile(ENV_CONFIG_PATH), (
        f"Missing file: {ENV_CONFIG_PATH}. "
        "You must create env_config.log before checking its contents."
    )
    with open(ENV_CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == ENV_CONFIG_EXPECTED_CONTENT, (
        f"env_config.log contents are incorrect.\n"
        "Expected exactly:\n"
        f"{ENV_CONFIG_EXPECTED_CONTENT!r}\n"
        f"But found:\n"
        f"{content!r}"
    )