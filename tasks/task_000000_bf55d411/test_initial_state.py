# test_initial_state.py

import os
import stat
import pytest

HOME = "/home/user"
ARTIFACT_REPO = os.path.join(HOME, "artifact_repo")
SCRIPTS_DIR = os.path.join(HOME, "scripts")
CURATION_LOGS_DIR = os.path.join(HOME, "curation_logs")

def file_nonempty(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0

def check_writable_dir(path):
    return os.path.isdir(path) and os.access(path, os.W_OK)

def check_executable_file(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def test_artifact_repo_structure():
    """Validate /home/user/artifact_repo/ and its project subdirectories/files exist as described."""
    assert os.path.isdir(ARTIFACT_REPO), (
        f"Directory {ARTIFACT_REPO} does not exist."
    )

    # project_alpha
    project_alpha = os.path.join(ARTIFACT_REPO, "project_alpha")
    assert os.path.isdir(project_alpha), (
        f"Directory {project_alpha} does not exist."
    )
    alpha_core_bin = os.path.join(project_alpha, "core.bin")
    alpha_runner_exe = os.path.join(project_alpha, "runner.exe")
    alpha_readme = os.path.join(project_alpha, "readme.txt")
    for path in [alpha_core_bin, alpha_runner_exe, alpha_readme]:
        assert file_nonempty(path), (
            f"File {path} does not exist or is empty."
        )

    # project_beta
    project_beta = os.path.join(ARTIFACT_REPO, "project_beta")
    assert os.path.isdir(project_beta), (
        f"Directory {project_beta} does not exist."
    )
    beta_notes = os.path.join(project_beta, "notes.md")
    assert file_nonempty(beta_notes), (
        f"File {beta_notes} does not exist or is empty."
    )
    # No .bin/.exe files in project_beta
    beta_bin_exe = [
        f for f in os.listdir(project_beta)
        if f.endswith(".bin") or f.endswith(".exe")
    ]
    assert not beta_bin_exe, (
        f"Expected no .bin or .exe files in {project_beta}, found: {beta_bin_exe}"
    )

    # project_gamma
    project_gamma = os.path.join(ARTIFACT_REPO, "project_gamma")
    assert os.path.isdir(project_gamma), (
        f"Directory {project_gamma} does not exist."
    )
    gamma_app_exe = os.path.join(project_gamma, "app.exe")
    gamma_module_bin = os.path.join(project_gamma, "module.bin")
    for path in [gamma_app_exe, gamma_module_bin]:
        assert file_nonempty(path), (
            f"File {path} does not exist or is empty."
        )

def test_scripts_dir_exists_and_writable():
    """Validate /home/user/scripts/ exists and is writable."""
    assert os.path.isdir(SCRIPTS_DIR), (
        f"Directory {SCRIPTS_DIR} does not exist."
    )
    assert os.access(SCRIPTS_DIR, os.W_OK), (
        f"Directory {SCRIPTS_DIR} is not writable."
    )

def test_curation_logs_dir_exists_and_writable():
    """Validate /home/user/curation_logs/ exists and is writable."""
    assert os.path.isdir(CURATION_LOGS_DIR), (
        f"Directory {CURATION_LOGS_DIR} does not exist."
    )
    assert os.access(CURATION_LOGS_DIR, os.W_OK), (
        f"Directory {CURATION_LOGS_DIR} is not writable."
    )

def test_no_output_files_present():
    """Ensure that the output script and log file do NOT yet exist before the task."""
    curate_script = os.path.join(SCRIPTS_DIR, "curate_artifacts.sh")
    artifact_log = os.path.join(CURATION_LOGS_DIR, "artifact_curation.log")
    assert not os.path.exists(curate_script), (
        f"Script {curate_script} should NOT exist before the task begins."
    )
    assert not os.path.exists(artifact_log), (
        f"Log file {artifact_log} should NOT exist before the task begins."
    )