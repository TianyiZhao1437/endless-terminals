# test_final_state.py

import os
import pytest

PIPELINE_DIR = '/home/user/pipeline'
INPUT_CSV = os.path.join(PIPELINE_DIR, 'input.csv')
OUTPUT_CSV = os.path.join(PIPELINE_DIR, 'output.csv')
PIPELINE_LOG = os.path.join(PIPELINE_DIR, 'pipeline.log')

EXPECTED_OUTPUT_CSV_LINES = [
    "alice,alice@example.com",
    "dan,dan@example.org"
]

EXPECTED_PIPELINE_LOG_LINES = [
    "[SUCCESS] Line 1: alice,alice@example.com",
    "[ERROR] Line 2: bob, - Missing fields",
    "[RECOVERY] Line 2: Skipped erroneous data.",
    "[ERROR] Line 3: charlie,charlie_at_example.com - Invalid email",
    "[RECOVERY] Line 3: Skipped erroneous data.",
    "[SUCCESS] Line 4: dan,dan@example.org"
]


def test_output_csv_exists_and_is_correct():
    assert os.path.isfile(OUTPUT_CSV), (
        f"Output file '{OUTPUT_CSV}' does not exist after pipeline completion.\n"
        "You must create this file with valid entries."
    )
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        output_lines = [line.rstrip('\n') for line in f]
    assert output_lines == EXPECTED_OUTPUT_CSV_LINES, (
        f"Output file '{OUTPUT_CSV}' has incorrect contents.\n"
        f"Expected:\n{EXPECTED_OUTPUT_CSV_LINES}\nActual:\n{output_lines}\n"
        "Ensure only valid entries are present, exactly as shown, with no extra or missing lines."
    )


def test_pipeline_log_exists_and_is_correct():
    assert os.path.isfile(PIPELINE_LOG), (
        f"Log file '{PIPELINE_LOG}' does not exist after pipeline completion.\n"
        "You must create this file to log processing outcomes."
    )
    with open(PIPELINE_LOG, 'r', encoding='utf-8') as f:
        log_lines = [line.rstrip('\n') for line in f]
    assert log_lines == EXPECTED_PIPELINE_LOG_LINES, (
        f"Log file '{PIPELINE_LOG}' has incorrect contents.\n"
        f"Expected:\n{EXPECTED_PIPELINE_LOG_LINES}\nActual:\n{log_lines}\n"
        "Log entries must strictly match templates, be in correct order, and contain no extra information."
    )


def test_input_csv_unchanged():
    # The input file must remain unmodified after task completion.
    assert os.path.isfile(INPUT_CSV), (
        f"Input file '{INPUT_CSV}' is missing after pipeline completion.\n"
        "Do not modify or remove the input file."
    )
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        input_lines = [line.rstrip('\n') for line in f]
    expected_input_lines = [
        "alice,alice@example.com",
        "bob,",
        "charlie,charlie_at_example.com",
        "dan,dan@example.org"
    ]
    assert input_lines == expected_input_lines, (
        f"Input file '{INPUT_CSV}' was modified during pipeline processing.\n"
        f"Expected contents:\n{expected_input_lines}\nActual:\n{input_lines}\n"
        "You must not alter the original input file."
    )


def test_no_extra_files_created():
    # Only input.csv, output.csv, and pipeline.log should exist in the directory after completion.
    expected_files = {'input.csv', 'output.csv', 'pipeline.log'}
    actual_files = set(os.listdir(PIPELINE_DIR))
    extra_files = actual_files - expected_files
    missing_files = expected_files - actual_files
    assert not missing_files, (
        f"Missing expected files in '{PIPELINE_DIR}': {missing_files}\n"
        "Ensure all required files are present after pipeline completion."
    )
    assert not extra_files, (
        f"Unexpected extra files found in '{PIPELINE_DIR}': {extra_files}\n"
        "Do not create any files other than input.csv, output.csv, and pipeline.log."
    )