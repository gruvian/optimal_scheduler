#!/bin/bash


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