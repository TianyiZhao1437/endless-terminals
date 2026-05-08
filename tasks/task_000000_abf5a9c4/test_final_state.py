# test_final_state.py
import os
import pytest
import stat

HOME = "/home/user"
ENV_PATH = "/home/user/.env"
ENV_LOG = "/home/user/env_check.log"
ML_DATA = "/home/user/ml_data"
TRAINING_SET = "/home/user/ml_data/training_set.csv"
MODELS = "/home/user/models"
MODEL_OUTPUT = "/home/user/models/model_v1.pth"

# Truth values for env
ENV_LINES = [
    f"DATASET_PATH={TRAINING_SET}",
    f"MODEL_OUTPUT={MODEL_OUTPUT}",
    "API_KEY=ml42keyAlphaSecure"
]

# Truth values for log
LOG_LINES = [
    TRAINING_SET,
    MODEL_OUTPUT,
    "ml42keyAlphaSecure"
]

def file_permissions_ok(filepath):
    st = os.stat(filepath)
    # Owner must have read/write, group/other can have nothing or read
    owner_rw = bool(st.st_mode & stat.S_IRUSR) and bool(st.st_mode & stat.S_IWUSR)
    # Check file is only readable/writable by user (mode 600 or 644 or 660 etc)
    return owner_rw and os.access(filepath, os.R_OK) and os.access(filepath, os.W_OK)

def test_env_file_exists_and_content():
    assert os.path.isfile(ENV_PATH), (
        f"'.env' file not found at '{ENV_PATH}'. "
        "Create the file in the home directory."
    )
    with open(ENV_PATH, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f]
    assert lines == ENV_LINES, (
        f"'.env' file content is incorrect.\n"
        f"Expected:\n  {ENV_LINES}\n"
        f"Found:\n  {lines}\n"
        "Ensure each variable is set exactly as specified, no extra spaces, quotes, or lines."
    )

def test_env_file_permissions():
    assert file_permissions_ok(ENV_PATH), (
        f"'.env' file at '{ENV_PATH}' does not have proper permissions. "
        "It must be readable and writable by the user. "
        "Set permissions to 600 or 644."
    )

def test_env_check_log_exists_and_content():
    assert os.path.isfile(ENV_LOG), (
        f"'env_check.log' file not found at '{ENV_LOG}'. "
        "Create the log file in the home directory."
    )
    with open(ENV_LOG, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f]
    assert lines == LOG_LINES, (
        f"'env_check.log' content is incorrect.\n"
        f"Expected:\n  {LOG_LINES}\n"
        f"Found:\n  {lines}\n"
        "Ensure each value is written exactly as specified, in order, one per line, no extra text or formatting."
    )

def test_env_check_log_permissions():
    assert file_permissions_ok(ENV_LOG), (
        f"'env_check.log' at '{ENV_LOG}' does not have proper permissions. "
        "It must be readable and writable by the user. "
        "Set permissions to 600 or 644."
    )

def test_no_extra_files_created():
    # Only .env and env_check.log must be newly created
    expected = {'.env', 'env_check.log'}
    found = set(os.listdir(HOME))
    # Ignore directories and known files
    ignore = {'ml_data', 'models',}
    extra = (found - expected) - ignore
    assert not extra or extra.issubset({'training_set.csv',}), (
        f"Extra files found in '{HOME}': {extra}. "
        "Do not create or modify any files other than '.env' and 'env_check.log' in the home directory."
    )

def test_ml_data_and_models_unchanged():
    # Ensure the training set and model directories are untouched (existence only)
    assert os.path.isdir(ML_DATA), (
        f"ML data directory '{ML_DATA}' is missing after task completion."
    )
    assert os.path.isfile(TRAINING_SET), (
        f"Training set file '{TRAINING_SET}' is missing after task completion."
    )
    assert os.path.isdir(MODELS), (
        f"Models directory '{MODELS}' is missing after task completion."
    )