# test_final_state.py
"""
Pytest suite to validate the FINAL state of the OS/filesystem after the student completes the benchmarking/logging task.
"""

import os
import stat
import pwd
import pytest

HOME = "/home/user"
BENCHMARKS_DIR = f"{HOME}/benchmarks"
LOG_FILE = f"{BENCHMARKS_DIR}/performance_tickets.log"

EXPECTED_LOG_CONTENT = """===
Ticket 1: CPU Benchmark
Events performed: 10000
Threads used: 2
Total time: 2.2032
Events per second: 4537.14

Ticket 2: Disk I/O Benchmark
Threads used: 2
Total bytes written: 134217728
Total time: 30.02
Throughput (MB/sec): 4.41
===
"""

@pytest.fixture(scope="module")
def user_uid_gid():
    """
    Returns the uid and gid for 'user'.
    """
    try:
        pw = pwd.getpwnam("user")
        return pw.pw_uid, pw.pw_gid
    except KeyError:
        pytest.skip("User 'user' does not exist on this system.")

def test_benchmarks_directory_exists(user_uid_gid):
    """
    /home/user/benchmarks directory must exist and be owned by user, with full read/write access.
    """
    assert os.path.isdir(BENCHMARKS_DIR), (
        f"The directory {BENCHMARKS_DIR} does not exist. "
        f"Create it to store benchmark logs."
    )

    st = os.stat(BENCHMARKS_DIR)
    expected_uid, expected_gid = user_uid_gid
    assert st.st_uid == expected_uid, (
        f"{BENCHMARKS_DIR} is owned by UID {st.st_uid}, but should be owned by user (UID {expected_uid})."
    )
    assert st.st_gid == expected_gid, (
        f"{BENCHMARKS_DIR} is group-owned by GID {st.st_gid}, but should be owned by user (GID {expected_gid})."
    )
    # Check user has rwx permissions
    mode = st.st_mode
    user_perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
    assert (mode & user_perms) == user_perms, (
        f"User does not have full read/write/execute permissions on {BENCHMARKS_DIR}."
    )

def test_benchmarks_directory_contents():
    """
    /home/user/benchmarks must contain ONLY performance_tickets.log and nothing else.
    """
    files = os.listdir(BENCHMARKS_DIR)
    assert files == ["performance_tickets.log"], (
        f"{BENCHMARKS_DIR} contains files other than performance_tickets.log: {files}. "
        f"Remove any extra files."
    )

def test_log_file_exists_and_permissions(user_uid_gid):
    """
    /home/user/benchmarks/performance_tickets.log must exist, owned by user, and be readable/writable by user.
    """
    assert os.path.isfile(LOG_FILE), (
        f"The log file {LOG_FILE} does not exist. "
        f"Create it with benchmark results."
    )
    st = os.stat(LOG_FILE)
    expected_uid, expected_gid = user_uid_gid
    assert st.st_uid == expected_uid, (
        f"{LOG_FILE} is owned by UID {st.st_uid}, but should be owned by user (UID {expected_uid})."
    )
    assert st.st_gid == expected_gid, (
        f"{LOG_FILE} is group-owned by GID {st.st_gid}, but should be owned by user (GID {expected_gid})."
    )
    user_perms = stat.S_IRUSR | stat.S_IWUSR
    assert (st.st_mode & user_perms) == user_perms, (
        f"User does not have full read/write permissions on {LOG_FILE}."
    )

def test_log_file_content_exact():
    """
    The log file must contain exactly the expected content, no extra or missing lines.
    """
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LOG_CONTENT, (
        "The contents of performance_tickets.log are incorrect.\n"
        "Expected exactly:\n"
        f"{EXPECTED_LOG_CONTENT}\n"
        "But found:\n"
        f"{content}\n"
        "Ensure you extract ONLY the specified metrics in the given template, without extra lines or missing values."
    )