import sys
import os
import threading
import toml
import rumps
import sounddevice as sd
from recorder import AudioRecorder
from transcriber import Transcriber
from typist import Typist
from hotkey import HotkeyListener
from cleaner import TextCleaner
from model_manager import ModelManager

class WhisperkeyApp(rumps.App):
    def __init__(self):
        super(WhisperkeyApp, self).__init__("⚪")
        
        # Load Config
        self.config = self.load_config()
        
        # Ensure model exists before starting
        try:
            self.model_path = ModelManager.ensure_model(self.config['model'])
        except Exception as e:
            rumps.alert("Model Error", f"Could not load model: {e}")
            sys.exit(1)
        
        # Initialize core components
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_path=self.model_path)
        self.typist = Typist()
        self.cleaner = TextCleaner()
        
        # State tracking
        self.is_recording = False
        
        # Menu setup
        model_options = [
            rumps.MenuItem("tiny.en", callback=self.set_model),
            rumps.MenuItem("base.en", callback=self.set_model),
            rumps.MenuItem("small.en", callback=self.set_model),
        ]
        self.model_menu = rumps.MenuItem(self.config['model'], model_options)
        
        self.menu = [
            rumps.MenuItem("About Whisperkey", callback=self.about_app),
            self.model_menu,
            rumps.separator,
            rumps.MenuItem("Quit", callback=self.quit_app),
        ]

        # Hotkey setup
        self.hotkey = HotkeyListener(
            on_press_callback=self.start_recording,
            on_release_callback=self.stop_and_type
        )
        self.hotkey_thread = threading.Thread(target=self.hotkey.start, daemon=True)
        self.hotkey_thread.start()

    def load_config(self):
        try:
            return toml.load("config.toml")
        except Exception:
            return {"model": "base.en", "hotkey": "right_option", "launch_at_login": False}

    def save_config(self):
        with open("config.toml", "w") as f:
            toml.dump(self.config, f)

    def set_model(self, sender):
        new_model = sender.title
        if new_model != self.config['model']:
            try:
                path = ModelManager.ensure_model(new_model)
                self.config['model'] = new_model
                self.save_config()
                self.transcriber = Transcriber(model_path=path)
                self.model_menu.title = new_model
                rumps.notification("Whisperkey", "Model Updated", f"Now using {new_model}")
            except Exception as e:
                rumps.alert("Model Error", f"Failed to switch model: {e}")

    def start_recording(self):
        if not self.is_recording:
            # Check mic access
            try:
                sd.query_devices()
            except Exception:
                rumps.alert("Microphone Error", "No microphone detected or permission denied.")
                return

            self.is_recording = True
            self.title = "🔴"
            self.recorder.start_recording()

    def stop_and_type(self):
        if self.is_recording:
            self.is_recording = False
            self.title = "⏳"
            threading.Thread(target=self._process_audio, daemon=True).start()

    def _process_audio(self):
        try:
            filename = self.recorder.stop_recording("temp_whisper.wav")
            text, _ = self.transcriber.transcribe(filename)
            cleaned_text = self.cleaner.clean(text)
            self.typist.paste_text(cleaned_text)
        except Exception as e:
            # Friendly error instead of terminal crash
            rumps.notification("Whisperkey Error", "Transcription failed", str(e))
        finally:
            self.title = "⚪"

    def about_app(self, _):
        rumps.alert("Whisperkey", "Local macOS dictation tool.\n\nHold Right Option, speak, and release to type.")

    def quit_app(self, _):
        self.hotkey.stop()
        rumps.app.quit()

if __name__ == "__main__":
    WhisperkeyApp().run()
