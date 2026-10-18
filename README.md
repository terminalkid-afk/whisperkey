# ⌨️ Whisperkey

### The Pro-Grade, Local, Open-Source Alternative to Paid Dictation.

**Whisperkey** is a high-performance macOS application that turns your voice into text instantly. No subscriptions, no cloud, and zero privacy risks. It runs entirely on your Mac, leveraging the power of Apple Silicon and `whisper.cpp`.

---

## 🌟 Why Whisperkey?

| Feature | Whisperkey | Paid Alternatives (Wispr Flow, etc.) |
| :--- | :--- | :--- |
| **Cost** | 💸 **Free Forever** | 💰 Expensive Monthly Subscriptions |
| **Privacy** | 🔒 **100% Local** | ☁️ Cloud-based (Your data leaves your Mac) |
| **Speed** | ⚡ **Instant** | 🐢 Network Latency |
| **Control** | 🛠️ **Open Source** | 🔒 Proprietary "Black Box" |

## 🚀 The Experience
1. **Hold** the `Right Option` key.
2. **Speak** naturally.
3. **Release** the key.
4. **Boom.** Your text is typed instantly into any active application.

## 🧠 Intelligence Under the Hood
- **Blazing Speed**: Optimized for M1/M2/M3 chips using `whisper.cpp`.
- **Clean Speech**: Automatically removes fillers like *"um"*, *"uh"*, and *"ah"*.
- **Voice Commands**: 
  - *"new line"* $\rightarrow$ `Enter`
  - *"period"* $\rightarrow$ `.`
  - *"comma"* $\rightarrow$ `,`
  - *"question mark"* $\rightarrow$ `?`
- **Smart Formatting**: Automatic sentence capitalization and trailing punctuation.

---

## 🛠️ Getting Started

### 1. Cloning the Repository
First, clone the project to your local machine:
```bash
git clone https://github.com/YOUR_USERNAME/whisperkey.git
cd whisperkey
```

### 2. Installation
We've made setup a one-click process. Run the setup script to create a virtual environment and install all dependencies:
```bash
bash setup.sh
```

### 3. Launching the App
To start Whisperkey, activate the environment and run the main script:
```bash
source venv/bin/activate
python main.py
```

## 🔒 Mandatory macOS Permissions
macOS blocks apps from listening to keys and recording audio by default. You **MUST** enable these in `System Settings` $\rightarrow$ `Privacy & Security`:

- **Microphone**: Enable your Terminal/App to allow voice capture.
- **Accessibility**: Enable your Terminal/App to allow simulating the `Cmd+V` paste.
- **Input Monitoring**: Enable your Terminal/App to allow the app to detect the `Right Option` hotkey globally.

> **Critical Tip:** If the hotkey doesn't work, remove your Terminal from "Input Monitoring" using the `[-]` button and add it back using the `[+]` button, then restart the terminal.

## ⚙️ Configuration
Customize your experience in `config.toml`:
- `model`: Choose `tiny.en` (Fastest), `base.en` (Balanced), or `small.en` (Most Accurate).
- `hotkey`: Change the trigger key.

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for more information.

---
**Built for speed. Built for privacy. Built for you.** 🚀
