#!/bin/bash

echo "🚀 Setting up Whisperkey..."

# Check for Python 3.11+
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" < "3.11" ]]; then
    echo "❌ Error: Python 3.11 or higher is required. You have $PYTHON_VERSION."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies (this may take a minute)..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully."
else
    echo "❌ Installation failed. Please check the errors above."
    exit 1
fi

echo ""
echo "==============================================================================="
echo "🎉 Setup Complete!"
echo "==============================================================================="
echo "To start Whisperkey, run:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "⚠️  IMPORTANT: Remember to grant macOS Permissions for:"
echo "  1. Microphone"
echo "  2. Accessibility"
echo "  3. Input Monitoring"
echo "==============================================================================="
