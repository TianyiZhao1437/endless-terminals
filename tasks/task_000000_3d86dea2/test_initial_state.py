# test_initial_state.py

import pytest
import os

PASSWD_PATH = "/etc/passwd"
SCAN_REPORT_PATH = "/home/user/scan_report.log"

@pytest.mark.parametrize("path", [PASSWD_PATH])
def test_passwd_file_exists(path):
    assert os.path.isfile(path), f"Required file '{path}' does not exist."

def test_passwd_file_permissions():
    import stat
    st = os.stat(PASSWD_PATH)
    # Check mode: -rw-r--r--
    expected_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    actual_mode = st.st_mode & 0o777
    assert actual_mode == 0o644, (
        f"/etc/passwd permissions are {oct(actual_mode)}, expected 0o644 (-rw-r--r--)."
    )
    # Check owner and group
    import pwd, grp
    owner = pwd.getpwuid(st.st_uid).pw_name
    group = grp.getgrgid(st.st_gid).gr_name
    assert owner == "root", f"/etc/passwd owner is '{owner}', expected 'root'."
    assert group == "root", f"/etc/passwd group is '{group}', expected 'root'."
    # Check file size
    assert st.st_size == 1234, (
        f"/etc/passwd size is {st.st_size}, expected 1234 bytes."
    )

def test_passwd_content_lines():
    with open(PASSWD_PATH, "r") as f:
        lines = f.readlines()
    expected_lines = [
        "root:x:0:0:root:/root:/bin/bash\n",
        "alice:x:1000:1000:Alice:/home/alice:/bin/bash\n",
        "bob:x:1001:1001:Bob:/home/bob:/usr/sbin/nologin\n",
        "eve:x:1002:1002:Eve:/home/eve:/bin/sh\n",
        "hacker:x:0:0:Hacker:/root:/bin/bash\n",
        "service:x:1003:1003:Service:/nonexistent:/usr/sbin/nologin\n",
    ]
    # Only check that all expected lines exist in the file (order matters)
    for idx, expected in enumerate(expected_lines):
        assert idx < len(lines), (
            f"/etc/passwd is missing expected line {idx+1}: {expected.strip()}"
        )
        actual = lines[idx]
        assert actual == expected, (
            f"/etc/passwd line {idx+1} is:\n  {actual.strip()}\nExpected:\n  {expected.strip()}"
        )

def test_scan_report_does_not_exist_yet():
    assert not os.path.exists(SCAN_REPORT_PATH), (
        f"Output file {SCAN_REPORT_PATH} already exists; it should not be present before the student starts."
    )