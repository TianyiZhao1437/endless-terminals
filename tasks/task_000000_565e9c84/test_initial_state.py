# test_initial_state.py

import os
import pytest

DEPLOYMENTS_DIR = "/home/user/deployments"
RELEASE_2_1_0_DIR = "/home/user/deployments/release_2.1.0"
CURRENT_SYMLINK = "/home/user/deployments/current"


def test_deployments_directory_exists():
    assert os.path.isdir(DEPLOYMENTS_DIR), (
        f"Missing required directory: {DEPLOYMENTS_DIR}"
    )

def test_release_2_1_0_directory_exists():
    assert os.path.isdir(RELEASE_2_1_0_DIR), (
        f"Missing required release directory: {RELEASE_2_1_0_DIR}"
    )

def test_current_symlink_exists_and_points_to_old_release():
    assert os.path.lexists(CURRENT_SYMLINK), (
        f"Missing required symlink: {CURRENT_SYMLINK}"
    )
    assert os.path.islink(CURRENT_SYMLINK), (
        f"{CURRENT_SYMLINK} exists but is not a symbolic link."
    )
    target = os.readlink(CURRENT_SYMLINK)
    # Accept either absolute or relative links, but not to release_2.1.0
    abs_target = os.path.abspath(os.path.join(os.path.dirname(CURRENT_SYMLINK), target))
    expected_new = os.path.abspath(RELEASE_2_1_0_DIR)
    if abs_target == expected_new:
        pytest.fail(
            f"{CURRENT_SYMLINK} already points to the new release directory; "
            "it should point to an old release before the task starts."
        )
    # It should point to some existing directory under /home/user/deployments/release_*
    # but NOT release_2.1.0
    assert abs_target.startswith(os.path.join(DEPLOYMENTS_DIR, "release_")), (
        f"{CURRENT_SYMLINK} points to {target}, which is not a release directory."
    )
    assert abs_target != expected_new, (
        f"{CURRENT_SYMLINK} already points to the new release directory; "
        "it should point to an old release before the task starts."
    )
    # Should exist
    assert os.path.isdir(abs_target), (
        f"{CURRENT_SYMLINK} points to {abs_target}, but that directory does not exist."
    )