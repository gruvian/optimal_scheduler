#!/bin/bash


EXECUTABLE_DIR="./dist/optimal_scheduler"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/OptimalScheduler.desktop"
INSTALL_DIR="$HOME/.local/share/OptimalScheduler"


mkdir -p "$INSTALL_DIR"


if [ -d "$EXECUTABLE_DIR" ]; then
    echo "Copying files to installation directory..."
    cp -r "$EXECUTABLE_DIR/"* "$INSTALL_DIR"

    
    chmod +x "$INSTALL_DIR/optimal_scheduler"

    
    cat > "$DESKTOP_FILE_PATH" <<EOL
[Desktop Entry]
Name=Optimal Scheduler
Exec=$INSTALL_DIR/optimal_scheduler
Icon=$INSTALL_DIR/logoLight.png
Type=Application
Terminal=false
Categories=Utility;
EOL

    
    chmod +x "$DESKTOP_FILE_PATH"

    echo "Launching Optimal Scheduler..."
    "$INSTALL_DIR/optimal_scheduler"

    echo "Installation complete."
else
    echo "Error: Executable directory not found at $EXECUTABLE_DIR"
    exit 1
fi
