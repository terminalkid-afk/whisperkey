import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Tuple

class AudioRecorder:
    """Handles recording audio from the microphone at 16kHz mono."""

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []

    def start_recording(self):
        """Starts capturing audio in chunks."""
        if self.recording:
            return

        self.recording = True
        self.audio_data = []

        # Force 16kHz, mono, float32
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=self._callback
        )
        self.stream.start()

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data.append(indata.copy())

    def stop_recording(self, filename: str = "temp_record.wav") -> str:
        """Stops recording and saves the captured audio to a WAV file."""
        self.recording = False
        self.stream.stop()
        self.stream.close()

        if not self.audio_data:
            raise RuntimeError("No audio data captured.")

        # Concatenate and ensure it's a numpy array
        recording_array = np.concatenate(self.audio_data, axis=0)
        
        # Force cast to float32 and ensure mono
        recording_array = recording_array.astype('float32')

        # Save as standard WAV with strict parameters
        sf.write(filename, recording_array, self.sample_rate, subtype='PCM_16')
        return filename
