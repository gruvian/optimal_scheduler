#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt update
    sudo apt install -y python3
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt install -y python3-pip
fi

pip3 install matplotlib pyqt5

# Define paths
EXECUTABLE_PATH="./dist/optimal_scheduler"
ICON_PATH="./icon.png"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/OptimalScheduler.desktop"
INSTALL_DIR="$HOME/.local/share/OptimalScheduler"

mkdir -p "$INSTALL_DIR"

cp "$EXECUTABLE_PATH" "$INSTALL_DIR"
cp "$ICON_PATH" "$INSTALL_DIR"

#debian .desktop file
cat > "$DESKTOP_FILE_PATH" <<EOL
[Desktop Entry]
Name=Optimal Scheduler
Exec=$INSTALL_DIR/optimal_scheduler
Icon=$INSTALL_DIR/icon.png
Type=Application
Terminal=false
Categories=Utility;
EOL


chmod +x "$DESKTOP_FILE_PATH"

echo "Launching Optimal Scheduler..."
$INSTALL_DIR/optimal_scheduler

echo "Installation complete."