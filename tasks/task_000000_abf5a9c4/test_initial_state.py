# test_initial_state.py
import os
import pytest
import stat

HOME = "/home/user"
ML_DATA = "/home/user/ml_data"
TRAINING_SET = "/home/user/ml_data/training_set.csv"
MODELS = "/home/user/models"


def test_home_directory_exists_and_writable():
    assert os.path.isdir(HOME), (
        f"Home directory '{HOME}' does not exist. "
        "Create the directory before proceeding."
    )
    assert os.access(HOME, os.W_OK), (
        f"Home directory '{HOME}' is not writable. "
        "Ensure you have write permissions."
    )


def test_ml_data_directory_and_training_set_exists():
    assert os.path.isdir(ML_DATA), (
        f"ML data directory '{ML_DATA}' does not exist. "
        "Create the directory before proceeding."
    )
    assert os.path.isfile(TRAINING_SET), (
        f"Training set file '{TRAINING_SET}' does not exist. "
        "Create the file before proceeding."
    )


def test_models_directory_exists_and_writable():
    assert os.path.isdir(MODELS), (
        f"Models directory '{MODELS}' does not exist. "
        "Create the directory before proceeding."
    )
    assert os.access(MODELS, os.W_OK), (
        f"Models directory '{MODELS}' is not writable. "
        "Ensure you have write permissions."
    )