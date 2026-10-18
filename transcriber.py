from pywhispercpp.model import Model
import time
from typing import Tuple
import collections

class Transcriber:
    """Integrates with whisper.cpp to transcribe audio files."""

    def __init__(self, model_path: str = "assets/ggml-base.en.bin"):
        self.model = Model(model=model_path)

    def transcribe(self, audio_path: str) -> Tuple[str, float]:
        start_time = time.perf_counter()
        
        # We use the transcribe method. If the model is stuttering, 
        # it's often because it's producing multiple segments for the same 
        # audio window.
        segments = self.model.transcribe(audio_path)
        
        if not segments:
            return "", time.perf_counter() - start_time

        # 1. STRICT TIMESTAMP DEDUPLICATION
        # We only keep segments that have a distinct start time.
        # If two segments start at the same time, they are definitely duplicates.
        unique_segments = []
        last_start = -1.0
        for s in segments:
            # Use getattr to safely access .start regardless of object/dict type
            start = getattr(s, 'start', None)
            if start is None and isinstance(s, dict):
                start = s.get('start', -1.0)
            
            if start != last_start:
                unique_segments.append(s)
                last_start = start

        # 2. TEXT EXTRACTION
        raw_texts = []
        for s in unique_segments:
            text = getattr(s, 'text', None)
            if text is None and isinstance(s, dict):
                text = s.get('text', '')
            if text and text.strip():
                raw_texts.append(text.strip())

        # 3. CONSECUTIVE TEXT DEDUPLICATION
        # Even with unique timestamps, Whisper sometimes "slides" and repeats.
        # If segment N is nearly identical to segment N-1, we drop it.
        final_texts = []
        for text in raw_texts:
            if not final_texts:
                final_texts.append(text)
                continue
            
            last = final_texts[-1].lower()
            curr = text.lower()
            
            # If current segment is a duplicate or a sub-string of the last one, skip it
            if curr == last or curr in last or last in curr:
                continue
            
            final_texts.append(text)

        full_text = " ".join(final_texts).strip()

        # 4. THE GLOBAL MIRROR CUT
        # If the final string is "Hello world. Hello world.", we cut it.
        if len(full_text) > 10:
            import re
            def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
            
            # Check if the first half matches the second half (fuzzy)
            mid = len(full_text) // 2
            if norm(full_text[:mid]) == norm(full_text[mid:]):
                full_text = full_text[:mid].strip()

        end_time = time.perf_counter()
        return full_text, end_time - start_time
