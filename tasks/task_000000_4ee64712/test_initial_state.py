# test_initial_state.py

import os
import pytest

HOME = "/home/user"
DATASETS = [
    os.path.join(HOME, "dataset1"),
    os.path.join(HOME, "dataset2"),
    os.path.join(HOME, "dataset3"),
]
BENCHMARK_LOG = os.path.join(HOME, "disk_benchmark.log")


@pytest.mark.parametrize("dataset_dir", DATASETS)
def test_dataset_directory_exists(dataset_dir):
    assert os.path.isdir(dataset_dir), (
        f"Required dataset directory '{dataset_dir}' does not exist. "
        f"Please ensure the directory is present before starting the task."
    )


@pytest.mark.parametrize("dataset_dir", DATASETS)
def test_dataset_directory_not_empty(dataset_dir):
    has_file = False
    for root, dirs, files in os.walk(dataset_dir):
        if files:
            has_file = True
            break
    assert has_file, (
        f"Dataset directory '{dataset_dir}' does not contain any files. "
        f"Each dataset directory must contain at least one file to perform a realistic benchmark."
    )


def test_benchmark_log_not_exists():
    assert not os.path.exists(BENCHMARK_LOG), (
        f"The benchmark log file '{BENCHMARK_LOG}' already exists. "
        f"Please remove it before starting the benchmarking task."
    )