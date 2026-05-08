import pytest
import os

API_RESPONSES_PATH = "/home/user/api_responses.txt"
EXTRACTED_IDS_PATH = "/home/user/extracted_ids.txt"

EXPECTED_API_RESPONSES_CONTENT = (
    '{"id":12,"status":"ok"}\n'
    '{"status":"error"}\n'
    '{"id":42,"status":"fail"}\n'
    '{"id":77,"status":"retry"}\n'
)

def test_api_responses_file_exists():
    assert os.path.isfile(API_RESPONSES_PATH), (
        f"Missing required input file: {API_RESPONSES_PATH}. "
        "You must have received this file before starting the task."
    )

def test_api_responses_file_content():
    with open(API_RESPONSES_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_API_RESPONSES_CONTENT, (
        f"The file {API_RESPONSES_PATH} does not contain the expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_API_RESPONSES_CONTENT!r}\n"
        "Actual:\n"
        f"{content!r}\n"
        "Please ensure the input file is exactly as described before beginning the task."
    )

def test_extracted_ids_file_absent():
    assert not os.path.exists(EXTRACTED_IDS_PATH), (
        f"The output file {EXTRACTED_IDS_PATH} should NOT exist before you begin the task.\n"
        "Please remove it if present, and start only with the input file."
    )