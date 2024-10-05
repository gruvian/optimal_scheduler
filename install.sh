#!/bin/bash

BASE_PATH=$(pwd)
EXECUTABLE_PATH="$BASE_PATH/dist/optimal_scheduler"
ICON_PATH="$BASE_PATH/icon.png"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/OptimalScheduler.desktop"
INSTALL_DIR="$HOME/.local/share/OptimalScheduler"

if [ ! -f "$EXECUTABLE_PATH" ]; then
    echo "Error: Executable not found at $EXECUTABLE_PATH"
    exit 1
fi

if [ ! -f "$ICON_PATH" ]; then
    echo "Error: Icon not found at $ICON_PATH"
    exit 1
fi

mkdir -p "$INSTALL_DIR"
cp "$EXECUTABLE_PATH" "$INSTALL_DIR"
cp "$ICON_PATH" "$INSTALL_DIR"

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