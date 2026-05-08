# test_initial_state.py

import os
import pytest

SCRAPE_LOG_PATH = "/home/user/scrape_audit.log"

def test_scrape_audit_log_does_not_exist():
    """
    The file /home/user/scrape_audit.log should NOT exist before the scraping task is performed.
    """
    assert not os.path.exists(SCRAPE_LOG_PATH), (
        f"Precondition failed: {SCRAPE_LOG_PATH} already exists. "
        f"Please remove this file before starting the task."
    )