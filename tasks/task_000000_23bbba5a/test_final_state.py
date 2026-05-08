# test_final_state.py

import os
import pytest

TABLES_LOG = '/home/user/deployment/logs/tables_list.log'
EXPECTED_TABLES = ['users', 'settings']


@pytest.mark.describe("Final state validation for SQLite tables list log")
class TestFinalState:
    def test_tables_list_log_exists(self):
        assert os.path.isfile(TABLES_LOG), (
            f"Missing required log file at {TABLES_LOG}. "
            "The file must be created by the task."
        )

    def test_tables_list_log_content_exact(self):
        """
        The log file must contain:
        - Exactly two lines: 'users' and 'settings'
        - In that order (users first, then settings)
        - No extra lines, blank lines, or trailing/leading whitespace
        - No headers, explanations, or extra content
        """
        with open(TABLES_LOG, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check for blank lines and strip line endings
        stripped_lines = [line.rstrip('\n').rstrip('\r') for line in lines]

        # Check for leading/trailing whitespace and blank lines
        for i, raw in enumerate(lines):
            stripped = stripped_lines[i]
            if raw != stripped + '\n' and raw != stripped + '\r\n':
                pytest.fail(
                    f"Line {i+1} in {TABLES_LOG} has unexpected whitespace: {repr(raw)}. "
                    "Each line must contain only the table name with no leading/trailing spaces."
                )
            if not stripped:
                pytest.fail(
                    f"Line {i+1} in {TABLES_LOG} is blank. "
                    "There must be no blank lines in the file."
                )

        # Check the number of lines
        assert len(stripped_lines) == len(EXPECTED_TABLES), (
            f"{TABLES_LOG} must contain exactly {len(EXPECTED_TABLES)} lines (one for each table). "
            f"Found {len(stripped_lines)} lines: {stripped_lines}"
        )

        # Check content and order
        assert stripped_lines == EXPECTED_TABLES, (
            f"{TABLES_LOG} contents are incorrect.\n"
            f"Expected lines (in order): {EXPECTED_TABLES}\n"
            f"Found lines: {stripped_lines}\n"
            "The file must contain only the table names, one per line, in the required order, with no extra content."
        )