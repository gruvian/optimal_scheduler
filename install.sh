#!/bin/bash

# root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

#pip
if ! command -v pip3 &>/dev/null; then
    echo "pip is not installed. Please install it first."
    exit 1
fi

#PyQt5
if ! python3 -c "import PyQt5" &>/dev/null; then
    echo "PyQt5 is not installed. Installing PyQt5..."
    pip3 install PyQt5
fi

#matplotlib
if ! python3 -c "import matplotlib" &>/dev/null; then
    echo "matplotlib is not installed. Installing matplotlib..."
    pip3 install matplotlib
fi

# directory for app
mkdir -p "$HOME/.local/share/optimalScheduler"

# cp files
cp "$SCRIPT_DIR/logoLight.png" "$HOME/.local/share/optimalScheduler/"
cp "$SCRIPT_DIR/logoDark.png" "$HOME/.local/share/optimalScheduler/"
cp "$SCRIPT_DIR/night_theme.css" "$HOME/.local/share/optimalScheduler/"
cp "$SCRIPT_DIR/day_theme.css" "$HOME/.local/share/optimalScheduler/"
cp "$SCRIPT_DIR/icon.png" "$HOME/.local/share/optimalScheduler/"

# ubuntu desktop file
cat <<EOF > "$HOME/.local/share/applications/optimalScheduler.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=Optimal Scheduler
Exec=python3 "$SCRIPT_DIR/optimal_scheduler.py"
Icon=$HOME/.local/share/optimalScheduler/icon.png
Terminal=false
Categories=Utility;
EOF

chmod +x "$HOME/.local/share/applications/optimalScheduler.desktop"

echo "Installation complete."
