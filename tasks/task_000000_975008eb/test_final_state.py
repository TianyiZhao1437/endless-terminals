# test_final_state.py

import os
import stat
import pytest
import pwd
import grp

SERVICE_STATUS_PATH = "/home/user/service_status_report.txt"
EXPECTED_OWNER = "user"
EXPECTED_GROUP = "user"
EXPECTED_PERMS = 0o644
EXPECTED_SERVICES = ["api_service", "web_service", "db_service"]

def read_status_report():
    """
    Read and return lines from the service status report file.
    """
    try:
        with open(SERVICE_STATUS_PATH, "r") as f:
            lines = f.readlines()
        return [line.rstrip("\n") for line in lines]
    except Exception as e:
        pytest.fail(f"Could not read {SERVICE_STATUS_PATH}: {e}")

def test_service_status_report_file_exists():
    """
    Ensure that the status report file exists after the task is completed.
    """
    assert os.path.exists(SERVICE_STATUS_PATH), (
        f"The file {SERVICE_STATUS_PATH} does not exist. "
        "You must create this file as part of your solution."
    )

def test_service_status_report_file_owner_group():
    """
    Ensure that the file is owned by user:user.
    """
    st = os.stat(SERVICE_STATUS_PATH)
    uid = st.st_uid
    gid = st.st_gid
    try:
        owner = pwd.getpwuid(uid).pw_name
    except KeyError:
        owner = f"<unknown uid {uid}>"
    try:
        group = grp.getgrgid(gid).gr_name
    except KeyError:
        group = f"<unknown gid {gid}>"
    assert owner == EXPECTED_OWNER, (
        f"{SERVICE_STATUS_PATH} is owned by '{owner}', expected '{EXPECTED_OWNER}'."
    )
    assert group == EXPECTED_GROUP, (
        f"{SERVICE_STATUS_PATH} is group-owned by '{group}', expected '{EXPECTED_GROUP}'."
    )

def test_service_status_report_file_permissions():
    """
    Ensure that the file has 644 permissions (rw-r--r--).
    """
    st = os.stat(SERVICE_STATUS_PATH)
    actual_perms = stat.S_IMODE(st.st_mode)
    assert actual_perms == EXPECTED_PERMS, (
        f"{SERVICE_STATUS_PATH} permissions are {oct(actual_perms)}, expected {oct(EXPECTED_PERMS)}."
    )

def test_service_status_report_file_format_and_content():
    """
    Ensure the file contains exactly three lines, one per service, in correct order and format.
    """
    lines = read_status_report()

    assert len(lines) == 3, (
        f"{SERVICE_STATUS_PATH} must contain exactly three lines, found {len(lines)}."
    )

    for i, service in enumerate(EXPECTED_SERVICES):
        expected_prefix = f"Service: {service} | Status: "
        assert lines[i].startswith(expected_prefix), (
            f"Line {i+1} in {SERVICE_STATUS_PATH} must start with '{expected_prefix}', "
            f"found: '{lines[i]}'"
        )
        status = lines[i][len(expected_prefix):]
        assert status in {"running", "stopped", "not_found"}, (
            f"Line {i+1} in {SERVICE_STATUS_PATH} has invalid status '{status}'. "
            "Valid statuses are: running, stopped, not_found."
        )

def test_service_status_report_file_no_extra_content():
    """
    Ensure the file contains only the required lines and no extra formatting or information.
    """
    lines = read_status_report()
    for i, line in enumerate(lines):
        # Must match exactly: Service: <name> | Status: <status>
        parts = line.split(" | ")
        assert len(parts) == 2, (
            f"Line {i+1} in {SERVICE_STATUS_PATH} is incorrectly formatted. "
            "Expected a single ' | ' separator."
        )
        left, right = parts
        assert left.startswith("Service: "), (
            f"Line {i+1} in {SERVICE_STATUS_PATH} must start with 'Service: '."
        )
        service_name = left[len("Service: "):]
        assert service_name in EXPECTED_SERVICES, (
            f"Line {i+1} in {SERVICE_STATUS_PATH} has unexpected service name '{service_name}'."
        )
        assert right.startswith("Status: "), (
            f"Line {i+1} in {SERVICE_STATUS_PATH} must contain 'Status: '."
        )
        status_value = right[len("Status: "):]
        assert status_value in {"running", "stopped", "not_found"}, (
            f"Line {i+1} in {SERVICE_STATUS_PATH} has invalid status '{status_value}'."
        )