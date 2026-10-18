#!/bin/bash
APP_PATH=$(pwd)
echo "Creating Whisperkey Launcher..."

cat << L_EOF > launch_whisperkey.sh
#!/bin/bash
source "$APP_PATH/venv/bin/activate"
python "$APP_PATH/main.py"
L_EOF

chmod +x launch_whisperkey.sh
echo "-------------------------------------------------------------------"
echo "✅ Launcher script created: launch_whisperkey.sh"
echo "-------------------------------------------------------------------"
echo "To turn this into a double-clickable macOS App:"
echo "1. Open 'Automator' (Cmd+Space -> Automator)"
echo "2. Select 'New Document' -> 'Application'"
echo "3. Search for 'Run Shell Script' and drag it into the workflow."
echo "4. Paste this exactly into the box:"
echo "$APP_PATH/launch_whisperkey.sh"
echo "5. Save it as 'Whisperkey.app' on your Desktop."
echo "-------------------------------------------------------------------"
