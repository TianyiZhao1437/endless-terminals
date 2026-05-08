# test_initial_state.py

import os
import pytest

PIPELINE_DIR = '/home/user/pipeline'
INPUT_CSV = os.path.join(PIPELINE_DIR, 'input.csv')


def test_pipeline_directory_exists_and_writable():
    assert os.path.isdir(PIPELINE_DIR), (
        f"Required directory '{PIPELINE_DIR}' does not exist. "
        "Please create it before proceeding."
    )
    assert os.access(PIPELINE_DIR, os.W_OK), (
        f"Directory '{PIPELINE_DIR}' is not writable. "
        "Ensure you have write permissions before proceeding."
    )


def test_input_csv_exists_with_correct_contents():
    assert os.path.isfile(INPUT_CSV), (
        f"Required input file '{INPUT_CSV}' does not exist. "
        "Please ensure the file is present before starting the task."
    )

    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    expected_lines = [
        "alice,alice@example.com",
        "bob,",
        "charlie,charlie_at_example.com",
        "dan,dan@example.org"
    ]
    assert lines == expected_lines, (
        f"File '{INPUT_CSV}' does not have the expected contents.\n"
        f"Expected:\n{expected_lines}\nActual:\n{lines}\n"
        "Please ensure the file matches the required input exactly, with no extra lines."
    )


def test_output_csv_does_not_exist_yet():
    output_csv = os.path.join(PIPELINE_DIR, 'output.csv')
    assert not os.path.exists(output_csv), (
        f"Output file '{output_csv}' should not exist before the task is started."
    )

def test_pipeline_log_does_not_exist_yet():
    pipeline_log = os.path.join(PIPELINE_DIR, 'pipeline.log')
    assert not os.path.exists(pipeline_log), (
        f"Log file '{pipeline_log}' should not exist before the task is started."
    )