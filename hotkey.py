from pynput import keyboard
from typing import Callable

class HotkeyListener:
    """Listens for the global hotkey (Right Option) to trigger recording."""

    def __init__(self, on_press_callback: Callable[[], None], on_release_callback: Callable[[], None]):
        self.on_press = on_press_callback
        self.on_release = on_release_callback
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def start(self):
        """Starts the global keyboard listener."""
        self.listener.start()

    def stop(self):
        """Stops the global keyboard listener."""
        self.listener.stop()

    def _on_press(self, key):
        # Right Option is typically detected as Key.alt or a specific vk code on macOS
        # In pynput, both left and right alt are often reported as Key.alt.
        # We check for the specific Right Option key if possible, 
        # otherwise we default to Alt for now and refine if needed.
        try:
            if key == keyboard.Key.alt or (hasattr(key, 'vk') and key.vk == 0x35):
                self.on_press()
        except Exception as e:
            print(f"Hotkey press error: {e}")

    def _on_release(self, key):
        try:
            if key == keyboard.Key.alt or (hasattr(key, 'vk') and key.vk == 0x35):
                self.on_release()
        except Exception as e:
            print(f"Hotkey release error: {e}")
