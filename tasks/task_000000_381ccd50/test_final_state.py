# test_final_state.py

import pytest
import os
import subprocess

CONF_PATH = "/home/user/mlops/artifact_service.conf"
EXPECTED_FINAL_CONTENT = "artifact_dir=/home/user/mlops/experiments/artifacts"
EXPECTED_OUTPUT = (
    f"Contents of /home/user/mlops/artifact_service.conf:\n"
    f"{EXPECTED_FINAL_CONTENT}"
)

def test_artifact_service_conf_exists():
    """Check that the artifact_service.conf file exists after the task."""
    assert os.path.isfile(CONF_PATH), (
        f"File missing: {CONF_PATH}. "
        "The configuration file must exist after completing the task."
    )

def test_artifact_service_conf_content():
    """Check that artifact_service.conf contains exactly the required content."""
    with open(CONF_PATH, "r") as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove any empty lines at the end
    lines = [line for line in lines if line.strip()]

    assert len(lines) == 1, (
        f"{CONF_PATH} must contain exactly one non-empty line after completion, "
        f"but found {len(lines)} line(s):\n" +
        "\n".join(lines)
    )
    assert lines[0] == EXPECTED_FINAL_CONTENT, (
        f"{CONF_PATH} content is incorrect.\n"
        f"Expected:\n{EXPECTED_FINAL_CONTENT}\n"
        f"Found:\n{lines[0]}"
    )

def test_no_extra_lines_in_conf():
    """Ensure no extra lines or whitespace in artifact_service.conf."""
    with open(CONF_PATH, "r") as f:
        contents = f.read()
    assert contents == EXPECTED_FINAL_CONTENT, (
        f"{CONF_PATH} must contain exactly:\n{EXPECTED_FINAL_CONTENT}\n"
        f"but found:\n{contents}\n"
        "Remove any extra lines, whitespace, or blank lines."
    )

def test_printed_output_matches_expected(monkeypatch):
    """
    Capture the output of the student's script and validate its exact format.
    This assumes the student's script is 'print_artifact_conf.py', or that
    the test runner will provide the script path via an environment variable.
    """
    # The student's script should be named or invoked in a way the test can locate.
    # Here we try to find a script to run; if not present, skip.
    script_candidates = [
        "print_artifact_conf.py",
        "/home/user/print_artifact_conf.py",
        "/workspace/print_artifact_conf.py",
        "task.py",
        "/home/user/task.py",
        "/workspace/task.py",
    ]
    script_path = None
    for candidate in script_candidates:
        if os.path.isfile(candidate):
            script_path = candidate
            break

    if script_path is None:
        pytest.skip(
            "No script found to check for printed output. "
            "Ensure the student's script is present in the workspace."
        )

    # Run the script and capture stdout, ensuring no extra output is present
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True,
        timeout=10
    )
    output = result.stdout.strip()
    assert result.returncode == 0, (
        f"The script did not exit cleanly (exit code {result.returncode}).\n"
        f"stderr:\n{result.stderr}"
    )
    assert output == EXPECTED_OUTPUT, (
        "The printed output does not match the required format.\n"
        f"Expected:\n{EXPECTED_OUTPUT}\n"
        f"Found:\n{output}\n"
        "Ensure your script prints only the required lines, with no extra whitespace or output."
    )
    assert result.stderr.strip() == "", (
        "Your script produced output to stderr:\n"
        f"{result.stderr}\n"
        "Ensure only the required output is printed to stdout, and no errors occur."
    )