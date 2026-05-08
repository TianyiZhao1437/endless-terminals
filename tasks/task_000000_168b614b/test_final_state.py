# test_final_state.py

import os
import json
import pytest

EXPERIMENT_SCRIPT = '/home/user/ml_projects/experiment_v1/run_experiment.py'
ARTIFACTS_DIR = '/home/user/ml_projects/experiment_v1/artifacts'
METRICS_JSON = os.path.join(ARTIFACTS_DIR, 'metrics.json')
MODEL_PKL = os.path.join(ARTIFACTS_DIR, 'model.pkl')
OUTPUT_LOG = os.path.join(ARTIFACTS_DIR, 'output.log')

EXPECTED_METRICS = {
    "accuracy": 0.962,
    "loss": 0.128
}
EXPECTED_OUTPUT_LOG_LINE = "Experiment completed successfully.\n"


def test_artifact_files_exist():
    missing = [p for p in [METRICS_JSON, MODEL_PKL, OUTPUT_LOG] if not os.path.isfile(p)]
    assert not missing, (
        "The following artifact files are missing after rerunning the experiment:\n"
        + "\n".join(missing)
        + "\nEnsure the experiment script overwrites and regenerates all required artifact files."
    )


def test_model_pkl_is_nonempty():
    size = os.path.getsize(MODEL_PKL) if os.path.exists(MODEL_PKL) else 0
    assert size > 0, (
        f"'{MODEL_PKL}' is missing or empty after rerunning the experiment.\n"
        "Ensure the script generates a non-empty model artifact."
    )


def test_output_log_contents():
    if not os.path.isfile(OUTPUT_LOG):
        pytest.fail(f"'{OUTPUT_LOG}' is missing after rerunning the experiment.")
    with open(OUTPUT_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_OUTPUT_LOG_LINE, (
        f"'{OUTPUT_LOG}' has incorrect contents after rerunning the experiment.\n"
        f"Expected exactly:\n{EXPECTED_OUTPUT_LOG_LINE!r}\nBut got:\n{content!r}\n"
        "Ensure the script overwrites this file with the correct output log."
    )


def test_metrics_json_structure_and_content(capsys):
    if not os.path.isfile(METRICS_JSON):
        pytest.fail(f"'{METRICS_JSON}' is missing after rerunning the experiment.")
    with open(METRICS_JSON, "r", encoding="utf-8") as f:
        content = f.read()

    # Display the exact JSON content to the terminal, as required
    print(content)

    try:
        data = json.loads(content)
    except Exception as e:
        pytest.fail(
            f"'{METRICS_JSON}' contains invalid JSON: {e}\n"
            "File contents:\n" + content
        )

    # Must contain exactly the expected keys
    missing_keys = [k for k in EXPECTED_METRICS if k not in data]
    extra_keys = [k for k in data if k not in EXPECTED_METRICS]
    assert not missing_keys, (
        f"'{METRICS_JSON}' is missing required keys: {missing_keys}\n"
        "File contents:\n" + content
    )
    assert not extra_keys, (
        f"'{METRICS_JSON}' contains unexpected keys: {extra_keys}\n"
        "File contents:\n" + content
    )

    # Values must be floats and match expected
    for key, expected_value in EXPECTED_METRICS.items():
        actual_value = data[key]
        assert isinstance(actual_value, float), (
            f"Key '{key}' in '{METRICS_JSON}' is not a float (got {type(actual_value).__name__}).\n"
            f"Value: {actual_value}\nFile contents:\n" + content
        )
        assert actual_value == expected_value, (
            f"Key '{key}' in '{METRICS_JSON}' has value {actual_value}, expected {expected_value}.\n"
            "File contents:\n" + content
        )

    # Check that the JSON is pretty-printed and matches the expected output exactly.
    # The required display/output is:
    # {
    #   "accuracy": 0.962,
    #   "loss": 0.128
    # }
    expected_json_str = '{\n  "accuracy": 0.962,\n  "loss": 0.128\n}'
    normalized_content = content.strip().replace('\r\n', '\n')
    assert normalized_content == expected_json_str, (
        f"'{METRICS_JSON}' does not match the required pretty-printed format.\n"
        "Expected:\n"
        + expected_json_str
        + "\nGot:\n"
        + normalized_content
        + "\nEnsure the script writes the JSON exactly in the required format."
    )