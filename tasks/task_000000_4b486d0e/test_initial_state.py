# test_initial_state.py

import os
import pytest

HOME = "/home/user"
TRANSLATIONS_DIR = os.path.join(HOME, "translations")
ES_DIR = os.path.join(TRANSLATIONS_DIR, "es")
MESSAGES_PO = os.path.join(ES_DIR, "messages.po")
UPDATE_LOG = os.path.join(TRANSLATIONS_DIR, "update_log.txt")

@pytest.mark.describe("Initial OS and filesystem state for translation update task")
class TestInitialState:
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

    def test_messages_po_initial_content(self):
        """
        Ensure /home/user/translations/es/messages.po has the expected pre-update content.
        """
        expected_lines = [
            'msgid "welcome"\n',
            'msgstr "Saludo de prueba"\n',
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
            f"{MESSAGES_PO} does not have the expected initial content.\n"
            "Expected:\n"
            + "".join(expected_lines)
            + "\nActual:\n"
            + "".join(actual_lines)
        )

    def test_update_log_does_not_exist(self):
        assert not os.path.exists(UPDATE_LOG), (
            f"{UPDATE_LOG} should NOT exist before the action. "
            "It must be created by the student after updating the translation."
        )