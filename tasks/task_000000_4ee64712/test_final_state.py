# test_final_state.py

import os
import re
import pytest

HOME = "/home/user"
DATASETS = [
    os.path.join(HOME, "dataset1"),
    os.path.join(HOME, "dataset2"),
    os.path.join(HOME, "dataset3"),
]
BENCHMARK_LOG = os.path.join(HOME, "disk_benchmark.log")

LOG_LINE_REGEX = re.compile(
    r"^(/home/user/dataset[123]) - ([0-9]+\.[0-9]{3})$"
)

@pytest.fixture(scope="module")
def log_lines():
    """Read and return the lines of the benchmark log file."""
    if not os.path.exists(BENCHMARK_LOG):
        pytest.fail(
            f"Benchmark log file '{BENCHMARK_LOG}' does not exist. "
            f"Expected file at the end of the task."
        )
    with open(BENCHMARK_LOG, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def test_benchmark_log_exists():
    assert os.path.isfile(BENCHMARK_LOG), (
        f"Benchmark log file '{BENCHMARK_LOG}' does not exist. "
        f"Expected the benchmarking results to be written to this file."
    )

def test_benchmark_log_line_count(log_lines):
    assert len(log_lines) == 3, (
        f"Benchmark log file '{BENCHMARK_LOG}' should contain EXACTLY three lines, "
        f"one for each dataset directory, but contains {len(log_lines)} lines."
    )

@pytest.mark.parametrize("expected_dir, line_no", [
    (DATASETS[0], 0),
    (DATASETS[1], 1),
    (DATASETS[2], 2),
])
def test_benchmark_log_line_format_and_order(log_lines, expected_dir, line_no):
    line = log_lines[line_no]
    m = LOG_LINE_REGEX.match(line)
    assert m is not None, (
        f"Line {line_no+1} of '{BENCHMARK_LOG}' ('{line}') is not in the correct format. "
        f"Expected: <directory> - <real_time> with exactly three decimals (e.g., "
        f"'/home/user/dataset1 - 0.123')."
    )
    dir_path, time_str = m.groups()
    assert dir_path == expected_dir, (
        f"Line {line_no+1} of '{BENCHMARK_LOG}' should refer to '{expected_dir}', "
        f"but found '{dir_path}'. Lines must be in the order: "
        f"/home/user/dataset1, /home/user/dataset2, /home/user/dataset3."
    )
    # float with exactly 3 decimals
    try:
        tval = float(time_str)
    except Exception:
        pytest.fail(
            f"Line {line_no+1} of '{BENCHMARK_LOG}' has an invalid timing value: '{time_str}'. "
            f"Must be a float with exactly three decimals."
        )
    # Ensure exactly three decimals (no more, no less, no scientific notation)
    assert re.fullmatch(r"[0-9]+\.[0-9]{3}", time_str), (
        f"Line {line_no+1} timing value '{time_str}' is not in the required format: "
        f"must be a floating point number with exactly three decimals (e.g., 0.123)."
    )
    # Optional: Ensure time is not negative or suspiciously high
    assert tval >= 0.0, (
        f"Line {line_no+1} timing value '{time_str}' must be non-negative."
    )

def test_benchmark_log_no_extra_content(log_lines):
    """Ensure there are no extra blank lines or trailing content."""
    with open(BENCHMARK_LOG, "rb") as f:
        content = f.read()
    # Ensure the file ends with the last line, no trailing newline
    assert content.endswith(log_lines[-1].encode()), (
        f"'{BENCHMARK_LOG}' should not have extra blank lines or trailing characters after the last result line."
    )