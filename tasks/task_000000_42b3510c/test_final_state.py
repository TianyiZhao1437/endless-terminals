# test_final_state.py

import os
import subprocess
import pytest

DB_PATH = "/home/user/monitoring_app/dashboards.db"
EXPECTED_OUTPUT = (
    "id          name             owner\n"
    "----------  ---------------  ------\n"
    "1           System Overview  alice\n"
    "2           Network Traffic  bob\n"
    "3           App Latency      carol\n"
)

@pytest.mark.describe("Final state validation after dashboard listing task")
class TestFinalState:

    def test_sqlite3_cli_lists_dashboards_table(self):
        """
        Validate that running the correct sqlite3 CLI command displays the dashboards table
        in the required tabular format with headers, and no output is saved to a file.
        """
        # Ensure the database exists at the absolute path
        assert os.path.isfile(DB_PATH), (
            f"Expected SQLite database at '{DB_PATH}', but it does not exist."
        )

        # Check that the sqlite3 CLI is available
        sqlite3_path = None
        for path in os.environ.get("PATH", "").split(os.pathsep):
            candidate = os.path.join(path, "sqlite3")
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                sqlite3_path = candidate
                break
        assert sqlite3_path is not None, (
            "The 'sqlite3' command-line client is not installed or not in PATH."
        )

        # Run the sqlite3 CLI with the expected command
        try:
            result = subprocess.run(
                [
                    sqlite3_path,
                    DB_PATH,
                    "-header",
                    "-column"
                ],
                input="SELECT * FROM dashboards;\n",
                text=True,
                capture_output=True,
                cwd=os.getcwd(),
                timeout=10
            )
        except FileNotFoundError:
            pytest.fail("The 'sqlite3' command-line client is not found on the system.")
        except subprocess.TimeoutExpired:
            pytest.fail("Timed out while running the 'sqlite3' CLI.")

        # Check for errors on stderr
        if result.stderr.strip():
            pytest.fail(
                f"Unexpected output on stderr from sqlite3:\n{result.stderr}"
            )

        # The output should match the expected format exactly
        actual_output = result.stdout
        # Remove any trailing whitespace or blank lines
        actual_output = actual_output.rstrip('\r\n')

        expected_output = EXPECTED_OUTPUT.rstrip('\n')

        assert actual_output == expected_output, (
            "The output of the sqlite3 command does not match the required format or content.\n"
            f"Expected output:\n{EXPECTED_OUTPUT}\n"
            f"Actual output:\n{actual_output}\n"
            "Ensure you:\n"
            "- Use 'sqlite3 /home/user/monitoring_app/dashboards.db -header -column'\n"
            "- Run 'SELECT * FROM dashboards;'\n"
            "- Output to the terminal (stdout) with no extra formatting, blank lines, or saved files."
        )