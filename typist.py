import pyperclip
import time
from pynput.keyboard import Controller, Key

class Typist:
    """Handles pasting transcribed text into the active application."""

    def __init__(self):
        self.keyboard = Controller()

    def paste_text(self, text: str):
        """
        Pastes text using the clipboard to ensure speed and 
        compatibility across all macOS apps.
        """
        if not text:
            return

        # 1. Save current clipboard
        original_clipboard = pyperclip.paste()

        try:
            # 2. Copy transcribed text to clipboard
            pyperclip.copy(text)

            # 3. Simulate Cmd+V
            with self.keyboard.pressed(Key.cmd):
                self.keyboard.press('v')
                self.keyboard.release('v')

            # Small delay to ensure macOS processes the paste before we restore
            time.sleep(0.1)

        finally:
            # 4. Restore original clipboard
            pyperclip.copy(original_clipboard)
