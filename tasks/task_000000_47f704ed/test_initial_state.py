# test_initial_state.py

import os
import pytest

MICROSERVICES_DIR = "/home/user/microservices"
EXPECTED_SERVICE_DIRS = {
    "auth_service",
    "billing_service",
    "user_service",
}

@pytest.mark.describe("Initial state of /home/user/microservices for microservice directory removal task")
def test_microservices_dir_exists():
    assert os.path.isdir(MICROSERVICES_DIR), (
        f"Required directory {MICROSERVICES_DIR} does not exist. "
        "Please ensure the microservices configuration root directory is present before starting."
    )

def test_microservices_dir_contains_expected_directories():
    """
    Ensure /home/user/microservices/ contains exactly the three expected microservice directories,
    and no extra directories (excluding hidden ones).
    """
    entries = os.listdir(MICROSERVICES_DIR)
    # Only non-hidden directories, not files or symlinks, and not entries starting with '.'
    found_dirs = {
        entry
        for entry in entries
        if not entry.startswith(".")
        and os.path.isdir(os.path.join(MICROSERVICES_DIR, entry))
        and not os.path.islink(os.path.join(MICROSERVICES_DIR, entry))
    }

    missing = EXPECTED_SERVICE_DIRS - found_dirs
    extra = found_dirs - EXPECTED_SERVICE_DIRS

    assert not missing, (
        f"Missing expected directories in {MICROSERVICES_DIR}: {', '.join(sorted(missing))}. "
        "Ensure all three directories are present: auth_service, billing_service, user_service."
    )
    assert not extra, (
        f"Found unexpected directories in {MICROSERVICES_DIR}: {', '.join(sorted(extra))}. "
        "Remove any directories that are not part of the expected set."
    )

def test_each_service_dir_is_directory():
    """
    Ensure each expected service directory exists and is a directory (not a file or symlink).
    """
    for dirname in EXPECTED_SERVICE_DIRS:
        full_path = os.path.join(MICROSERVICES_DIR, dirname)
        assert os.path.exists(full_path), (
            f"Expected directory {full_path} does not exist."
        )
        assert os.path.isdir(full_path), (
            f"{full_path} exists but is not a directory."
        )
        assert not os.path.islink(full_path), (
            f"{full_path} is a symbolic link, not a real directory."
        )