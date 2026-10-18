from setuptools import setup

APP = ['main.py']
DATA_FILES = [('assets', ['assets/ggml-base.en.bin'])]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rumps', 'pywhispercpp', 'sounddevice', 'soundfile', 'pynput', 'pyperclip', 'toml', 'numpy', 'requests', 'tqdm'],
    'plist': {
        'CFBundleName': 'Whisperkey',
        'CFBundleDisplayName': 'Whisperkey',
        'CFBundleIdentifier': 'com.namangupta.whisperkey',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app.options': OPTIONS},
    setup_requires=['py2app'],
)
