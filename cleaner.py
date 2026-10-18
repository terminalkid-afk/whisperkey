import re
from typing import List

class TextCleaner:
    """Cleans up transcribed text by removing fillers, handling voice commands, 
    and fixing basic formatting.
    """

    def __init__(self):
        # Filler words to remove
        self.fillers = [
            r"\bum\b", r"\buh\b", r"\bah\b", r"\ber\b", r"\buhm\b"
        ]
        
        # Voice commands mapping
        self.commands = {
            "new line": "\n",
            "period": ".",
            "comma": ",",
            "question mark": "?",
            "exclamation mark": "!",
        }

    def clean(self, text: str) -> str:
        if not text:
            return ""

        # 1. Fix duplication: If text repeats itself (e.g., "Hello Hello" or "Sentence. Sentence.")
        # We check if the first half is nearly identical to the second half
        text = self._remove_duplications(text)

        # 2. Handle Voice Commands
        # Case-insensitive replacement for commands like "new line"
        for cmd, symbol in self.commands.items():
            # Use regex for case-insensitive replacement of whole phrases
            text = re.sub(rf"\b{cmd}\b", symbol, text, flags=re.IGNORECASE)

        # 3. Remove Filler Words
        for filler in self.fillers:
            text = re.sub(filler, "", text, flags=re.IGNORECASE)

        # 4. Basic Formatting
        # Remove extra spaces created by filler removal
        text = re.sub(r'\s+', ' ', text).strip()

        if text:
            # Capitalize first letter
            text = text[0].upper() + text[1:] if len(text) > 0 else text
            
            # Ensure it ends with a punctuation mark if it doesn't have one
            if text and text[-1] not in {'.', '?', '!', '\n'}:
                text += "."

        return text

    def _remove_duplications(self, text: str) -> str:
        """Detects and removes identical repeating patterns in the text."""
        trimmed = text.strip()
        if len(trimmed) < 10:
            return text

        # 1. Exact Repetition Detection (Mirroring)
        # If the string is "Hello Hello" or "I like Xbox. I like Xbox."
        # We check for the longest repeating sequence that makes up the string.

        # Try splitting in half
        mid = len(trimmed) // 2
        first_half = trimmed[:mid].strip().lower()
        second_half = trimmed[mid:].strip().lower()

        # We use a normalized comparison to ignore punctuation differences
        def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

        if norm(first_half) == norm(second_half) and len(norm(first_half)) > 5:
            return trimmed[:mid].strip()

        # 2. Sequence-based pruning
        # If the text contains the same phrase twice in a row
        # Example: "I love Mac. I love Mac."
        # We look for the first occurrence of a significant phrase and see if it repeats.
        words = trimmed.split()
        if len(words) >= 4:
            # Check for repeating halves of word lists
            half = len(words) // 2
            if words[:half] == words[half:]:
                return " ".join(words[:half])

        return text



