# test_final_state.py

import os
import pytest

MICROSERVICES_DIR = "/home/user/microservices"
AUTH_SERVICE_DIR = os.path.join(MICROSERVICES_DIR, "auth_service")
BILLING_SERVICE_DIR = os.path.join(MICROSERVICES_DIR, "billing_service")
USER_SERVICE_DIR = os.path.join(MICROSERVICES_DIR, "user_service")
DIRS_AFTER_REMOVAL_FILE = "/home/user/microservice_dirs_after_removal.txt"

EXPECTED_DIRS = {"billing_service", "user_service"}
EXPECTED_FILE_CONTENTS = "billing_service\nuser_service\n"

@pytest.mark.describe("Final state after removing the deprecated auth_service microservice directory")
def test_auth_service_dir_is_removed():
    """
    Verify that /home/user/microservices/auth_service no longer exists.
    """
    assert not os.path.exists(AUTH_SERVICE_DIR), (
        f"The deprecated directory {AUTH_SERVICE_DIR} still exists. "
        "It must be fully deleted, including all its contents."
    )

def test_other_service_dirs_exist_and_are_directories():
    """
    Ensure billing_service and user_service directories still exist,
    are directories, and are not symlinks.
    """
    for dirname in EXPECTED_DIRS:
        full_path = os.path.join(MICROSERVICES_DIR, dirname)
        assert os.path.exists(full_path), (
            f"Expected directory {full_path} is missing after auth_service removal. "
            "Do not delete or modify other microservice directories."
        )
        assert os.path.isdir(full_path), (
            f"{full_path} exists but is not a directory. "
            "Ensure only directories remain for each microservice."
        )
        assert not os.path.islink(full_path), (
            f"{full_path} is a symbolic link, not a real directory. "
            "Symlinks are not permitted for microservice directories."
        )

def test_no_extra_service_dirs_present():
    """
    Check that only billing_service and user_service remain in /home/user/microservices,
    and no extra non-hidden directories are present.
    """
    entries = os.listdir(MICROSERVICES_DIR)
    found_dirs = {
        entry
        for entry in entries
        if not entry.startswith(".")
        and os.path.isdir(os.path.join(MICROSERVICES_DIR, entry))
        and not os.path.islink(os.path.join(MICROSERVICES_DIR, entry))
    }

    missing = EXPECTED_DIRS - found_dirs
    extra = found_dirs - EXPECTED_DIRS

    assert not missing, (
        f"Missing expected directories in {MICROSERVICES_DIR}: {', '.join(sorted(missing))}. "
        "After removal, billing_service and user_service must still exist."
    )
    assert not extra, (
        f"Unexpected directories found in {MICROSERVICES_DIR}: {', '.join(sorted(extra))}. "
        "Only billing_service and user_service should remain after auth_service removal."
    )

def test_dirs_after_removal_file_exists():
    """
    Verify that the output file /home/user/microservice_dirs_after_removal.txt exists.
    """
    assert os.path.isfile(DIRS_AFTER_REMOVAL_FILE), (
        f"Required output file {DIRS_AFTER_REMOVAL_FILE} does not exist. "
        "You must create this file listing all remaining microservice directories."
    )

def test_dirs_after_removal_file_content():
    """
    Verify that the output file contains exactly the sorted directory names,
    one per line, with no extra whitespace, blank lines, paths, or hidden directories.
    """
    with open(DIRS_AFTER_REMOVAL_FILE, "r", encoding="utf-8") as f:
        lines = f.read()

    assert lines == EXPECTED_FILE_CONTENTS, (
        f"The contents of {DIRS_AFTER_REMOVAL_FILE} are incorrect.\n"
        f"Expected exactly:\n{EXPECTED_FILE_CONTENTS!r}\n"
        f"But found:\n{lines!r}\n"
        "Ensure the file contains only the sorted directory names (billing_service and user_service), "
        "one per line, with no blank lines, extra whitespace, hidden directories, or paths."
    )