# test_initial_state.py

import os
import pytest

EXPERIMENT_SCRIPT = '/home/user/ml_projects/experiment_v1/run_experiment.py'
ARTIFACTS_DIR = '/home/user/ml_projects/experiment_v1/artifacts'
METRICS_JSON = os.path.join(ARTIFACTS_DIR, 'metrics.json')
MODEL_PKL = os.path.join(ARTIFACTS_DIR, 'model.pkl')
OUTPUT_LOG = os.path.join(ARTIFACTS_DIR, 'output.log')

@pytest.mark.parametrize("path", [
    EXPERIMENT_SCRIPT,
    METRICS_JSON,
    MODEL_PKL,
    OUTPUT_LOG,
])
def test_required_files_exist(path):
    assert os.path.isfile(path), (
        f"Missing required file: '{path}'.\n"
        "Ensure the experiment script and all artifact files exist before proceeding."
    )

def test_artifacts_directory_exists():
    assert os.path.isdir(ARTIFACTS_DIR), (
        f"Missing required directory: '{ARTIFACTS_DIR}'.\n"
        "Ensure the 'artifacts' directory exists before running the experiment."
    )