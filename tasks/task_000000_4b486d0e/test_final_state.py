# test_final_state.py

import os
import pytest

HOME = "/home/user"
TRANSLATIONS_DIR = os.path.join(HOME, "translations")
ES_DIR = os.path.join(TRANSLATIONS_DIR, "es")
MESSAGES_PO = os.path.join(ES_DIR, "messages.po")
UPDATE_LOG = os.path.join(TRANSLATIONS_DIR, "update_log.txt")

@pytest.mark.describe("Final OS and filesystem state after translation update task")
class TestFinalState:
    def test_translations_directory_exists(self):
        assert os.path.isdir(TRANSLATIONS_DIR), (
            f"Required directory not found: {TRANSLATIONS_DIR}"
        )

    def test_es_directory_exists(self):
        assert os.path.isdir(ES_DIR), (
            f"Required directory not found: {ES_DIR}"
        )

    def test_messages_po_exists(self):
        assert os.path.isfile(MESSAGES_PO), (
            f"Required file not found: {MESSAGES_PO}"
        )

    def test_messages_po_final_content(self):
        """
        Ensure /home/user/translations/es/messages.po has the expected post-update content.
        """
        expected_lines = [
            'msgid "welcome"\n',
            'msgstr "Bienvenido"\n',
            '\n',
            'msgid "exit"\n',
            'msgstr "Salir"\n',
        ]
        try:
            with open(MESSAGES_PO, encoding="utf-8") as f:
                actual_lines = f.readlines()
        except Exception as e:
            pytest.fail(f"Could not read {MESSAGES_PO}: {e}")

        assert actual_lines == expected_lines, (
            f"{MESSAGES_PO} does not have the expected final content after update.\n"
            "Expected content:\n"
            + "".join(expected_lines)
            + "\nActual content:\n"
            + "".join(actual_lines)
            + "\n\n"
            "If the 'welcome' msgstr was not updated to 'Bienvenido', or if the formatting/spacing is incorrect, "
            "please check your editing logic."
        )

    def test_update_log_exists(self):
        assert os.path.isfile(UPDATE_LOG), (
            f"{UPDATE_LOG} was not created. "
            "You must create this file after updating the translation."
        )

    def test_update_log_exact_content(self):
        """
        The log file must have exactly two lines, with exact text and UNIX line endings.
        """
        expected_lines = [
            "Updated msgid \"welcome\" in messages.po\n",
            "New translation: Bienvenido\n",
        ]
        try:
            with open(UPDATE_LOG, "rb") as f:
                raw_bytes = f.read()
            # Check for CRLF, must not be present
            if b"\r\n" in raw_bytes:
                pytest.fail(
                    f"{UPDATE_LOG} uses Windows (CRLF) line endings. "
                    "It must use UNIX (LF) line endings only."
                )
            # Now decode and split into lines
            text = raw_bytes.decode("utf-8")
            actual_lines = text.splitlines(keepends=True)
        except Exception as e:
            pytest.fail(f"Could not read {UPDATE_LOG}: {e}")

        # Check for exact number of lines
        assert len(actual_lines) == 2, (
            f"{UPDATE_LOG} must contain exactly two lines, but found {len(actual_lines)}.\n"
            "Actual content:\n"
            + "".join(actual_lines)
        )

        # Check for exact content and no extra whitespace
        for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines), 1):
            assert actual == expected, (
                f"{UPDATE_LOG} line {i} is incorrect.\n"
                f"Expected: {repr(expected)}\nGot:      {repr(actual)}\n"
                "Check for typos, whitespace, or incorrect line endings."
            )