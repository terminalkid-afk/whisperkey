import time
import os
from recorder import AudioRecorder
from transcriber import Transcriber
from pynput import keyboard

def main():
    print("--- Whisperkey Phase 1 Test ---")
    
    # Setup
    recorder = AudioRecorder()
    # We assume the model is in assets/ggml-base.en.bin
    model_path = "assets/ggml-base.en.bin"
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please place the ggml-base.en.bin file in the assets/ folder.")
        return

    transcriber = Transcriber(model_path=model_path)
    
    print("\nInstructions:")
    print("1. Hold the 'S' key to record your voice.")
    print("2. Release the 'S' key to stop and transcribe.")
    print("3. Press 'Esc' to exit the test script.")

    recording = False

    def on_press(key):
        nonlocal recording
        try:
            if key.char == 's' and not recording:
                print("\n🔴 Recording... (Release 'S' to stop)")
                recorder.start_recording()
                recording = True
        except AttributeError:
            pass

    def on_release(key):
        nonlocal recording
        try:
            if key.char == 's' and recording:
                print("⏹️ Stopped. Transcribing...")
                recording = False
                
                try:
                    filename = recorder.stop_recording("phase1_temp.wav")
                    text, elapsed = transcriber.transcribe(filename)
                    print(f"📝 Transcription: {text}")
                    print(f"⏱️ Speed: {elapsed:.2f} seconds")
                except Exception as e:
                    print(f"❌ Error: {e}")
        except AttributeError:
            pass
        
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
