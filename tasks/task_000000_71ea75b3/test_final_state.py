# test_final_state.py

import os
import pytest

CONFIG_PATH = "/home/user/build/config_android.txt"
UTF8_OUTPUT_PATH = "/home/user/build/config_android_utf8.txt"
LOG_PATH = "/home/user/build/encoding_conversion.log"

# The expected content, as Unicode text (as it should appear after conversion)
EXPECTED_TEXT = (
    "name=André\n"
    "mode=Desenvolvimento\n"
    "api=29\n"
)

# The expected log entry, exactly as required
EXPECTED_LOG_LINE = (
    "config_android.txt converted from ISO-8859-1 to UTF-8 as config_android_utf8.txt\n"
)

@pytest.mark.describe("Final OS/filesystem state after encoding conversion")
class TestFinalState:
    def test_utf8_output_file_exists(self):
        assert os.path.isfile(UTF8_OUTPUT_PATH), (
            f"Missing output file: {UTF8_OUTPUT_PATH}. "
            "The converted UTF-8 configuration file must exist after the task."
        )

    def test_utf8_output_file_content_and_encoding(self):
        """
        Validates that /home/user/build/config_android_utf8.txt:
        - Is encoded in UTF-8 (é as 0xc3 0xa9)
        - Contains the exact expected text content
        - No extra bytes or lines
        """
        # Read as binary and check UTF-8 encoding and byte sequence for 'é'
        try:
            with open(UTF8_OUTPUT_PATH, "rb") as f:
                content_bytes = f.read()
        except Exception as e:
            pytest.fail(f"Could not read {UTF8_OUTPUT_PATH}: {e}")

        # Decode as UTF-8, fail if decoding error
        try:
            decoded = content_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(
                f"{UTF8_OUTPUT_PATH} is not valid UTF-8: {e}\n"
                "File must be encoded in UTF-8."
            )

        assert decoded == EXPECTED_TEXT, (
            f"{UTF8_OUTPUT_PATH} content does not match the expected UTF-8 text.\n"
            "Expected:\n" + EXPECTED_TEXT +
            "\nGot:\n" + decoded
        )

        # Check that the byte sequence for 'é' is UTF-8 (0xc3 0xa9)
        # Find 'André' and 'Desenvolvimento' in bytes
        expected_bytes = (
            b"name=Andr\xc3\xa9\n"
            b"mode=Desenvolvimento\n"
            b"api=29\n"
        )
        assert content_bytes == expected_bytes, (
            f"{UTF8_OUTPUT_PATH} does not have correct UTF-8 encoding for special characters.\n"
            "Expected bytes:\n" + str(expected_bytes) +
            "\nGot bytes:\n" + str(content_bytes)
        )

    def test_log_file_exists(self):
        assert os.path.isfile(LOG_PATH), (
            f"Missing log file: {LOG_PATH}. "
            "The log file must be created after the conversion."
        )

    def test_log_file_content(self):
        """
        Validates that /home/user/build/encoding_conversion.log contains EXACTLY the required line.
        """
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                log_content = f.read()
        except Exception as e:
            pytest.fail(f"Could not read {LOG_PATH}: {e}")

        assert log_content == EXPECTED_LOG_LINE, (
            f"{LOG_PATH} content is incorrect.\n"
            "Expected:\n" + EXPECTED_LOG_LINE +
            "Got:\n" + log_content +
            "\nThe log file must contain exactly one line, as specified."
        )

    def test_utf8_output_printed_to_terminal(self, capsys):
        """
        This test assumes the student's script prints the contents of config_android_utf8.txt to stdout.
        Since pytest cannot verify external script output, this test demonstrates how to check print output
        if the student's code is run within pytest. If not, this test will be skipped.
        """
        # Only run if the student's script is invoked in pytest and prints the file contents.
        # We'll skip this test unless explicitly required by the pipeline.
        pytest.skip("Terminal print output cannot be verified from outside the student's script. "
                    "If you want to check print output, use capsys in your script tests.")