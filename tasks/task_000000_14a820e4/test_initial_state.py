# test_initial_state.py

import os
import pytest

HOME = "/home/user"
CONFIGS_DIR = os.path.join(HOME, "services", "configs")
OUTPUT_DIR = os.path.join(HOME, "services", "output")
INI_PATH = os.path.join(CONFIGS_DIR, "microservice.ini")

EXPECTED_INI_CONTENT = (
    "[service]\n"
    "name=auth\n"
    "port=8081\n"
    "\n"
    "[database]\n"
    "host=db.internal\n"
    "port=5432\n"
)

def test_configs_dir_exists_and_writable():
    assert os.path.isdir(CONFIGS_DIR), (
        f"Required directory not found: {CONFIGS_DIR}"
    )
    assert os.access(CONFIGS_DIR, os.W_OK), (
        f"Directory is not writable: {CONFIGS_DIR}"
    )

def test_output_dir_exists_and_writable():
    assert os.path.isdir(OUTPUT_DIR), (
        f"Required directory not found: {OUTPUT_DIR}"
    )
    assert os.access(OUTPUT_DIR, os.W_OK), (
        f"Directory is not writable: {OUTPUT_DIR}"
    )

def test_microservice_ini_exists_and_content():
    assert os.path.isfile(INI_PATH), (
        f"Required INI file not found: {INI_PATH}"
    )
    with open(INI_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_INI_CONTENT, (
        f"INI file {INI_PATH} does not contain the expected content.\n"
        "Expected content:\n"
        f"{EXPECTED_INI_CONTENT!r}\n"
        "Actual content:\n"
        f"{actual_content!r}"
    )