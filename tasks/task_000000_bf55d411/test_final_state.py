# test_final_state.py

import os
import stat
import pytest

HOME = "/home/user"
ARTIFACT_REPO = os.path.join(HOME, "artifact_repo")
SCRIPTS_DIR = os.path.join(HOME, "scripts")
CURATION_LOGS_DIR = os.path.join(HOME, "curation_logs")

CURATE_SCRIPT = os.path.join(SCRIPTS_DIR, "curate_artifacts.sh")
CURATION_LOG = os.path.join(CURATION_LOGS_DIR, "artifact_curation.log")

EXPECTED_LOG_CONTENTS = (
    "Project: project_alpha\n"
    "/home/user/artifact_repo/project_alpha/core.bin\n"
    "/home/user/artifact_repo/project_alpha/runner.exe\n"
    "\n"
    "Project: project_beta\n"
    "No artifacts found.\n"
    "\n"
    "Project: project_gamma\n"
    "/home/user/artifact_repo/project_gamma/app.exe\n"
    "/home/user/artifact_repo/project_gamma/module.bin\n"
    "\n"
)

def test_script_exists_and_is_executable():
    """Check that the curate_artifacts.sh script exists and is executable."""
    assert os.path.isfile(CURATE_SCRIPT), (
        f"Script {CURATE_SCRIPT} does not exist."
    )
    st = os.stat(CURATE_SCRIPT)
    # Check owner execute bit (user should have execute)
    assert st.st_mode & stat.S_IXUSR, (
        f"Script {CURATE_SCRIPT} exists but is not executable by the user."
    )

def test_log_file_exists_and_is_file():
    """Check that the artifact_curation.log exists and is a file."""
    assert os.path.isfile(CURATION_LOG), (
        f"Log file {CURATION_LOG} does not exist or is not a regular file."
    )

def test_log_file_contents_exact():
    """Check that the log file contents exactly match the required format and data."""
    with open(CURATION_LOG, "r", encoding="utf-8") as f:
        actual = f.read()
    assert actual == EXPECTED_LOG_CONTENTS, (
        f"Log file {CURATION_LOG} contents are incorrect.\n"
        f"--- Expected ---\n{EXPECTED_LOG_CONTENTS!r}\n"
        f"--- Actual ---\n{actual!r}\n"
        "If the log differs in whitespace, order, or file listing, fix your script to match the specification exactly."
    )

def test_log_file_permissions():
    """Check that the log file is writable by the user."""
    assert os.access(CURATION_LOG, os.W_OK), (
        f"Log file {CURATION_LOG} is not writable by the user."
    )

def test_script_file_permissions():
    """Check that the script is readable and executable by the user."""
    assert os.access(CURATE_SCRIPT, os.R_OK), (
        f"Script {CURATE_SCRIPT} is not readable by the user."
    )
    assert os.access(CURATE_SCRIPT, os.X_OK), (
        f"Script {CURATE_SCRIPT} is not executable by the user."
    )

def test_log_file_no_extra_content():
    """Check that there is no extra content after the last newline."""
    with open(CURATION_LOG, "rb") as f:
        contents = f.read()
    # The last character must be a single newline and nothing after
    assert contents.endswith(b"\n"), (
        f"Log file {CURATION_LOG} does not end with a newline."
    )
    # Should only be a single trailing newline
    assert not contents.endswith(b"\n\n"), (
        f"Log file {CURATION_LOG} has extra blank lines at the end."
    )

def test_script_shebang_and_syntax():
    """Check that the shell script starts with a valid shebang."""
    with open(CURATE_SCRIPT, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    assert first_line.startswith("#!"), (
        f"Script {CURATE_SCRIPT} does not start with a shebang (#!)."
    )
    # Accept any bash/sh, but must be a shell script
    assert "sh" in first_line or "bash" in first_line, (
        f"Script {CURATE_SCRIPT} does not use a shell interpreter in its shebang: {first_line!r}"
    )