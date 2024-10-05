#!/bin/bash

INSTALL_DIR="$HOME/.local/share/OptimalScheduler"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/OptimalScheduler.desktop"

# Confirmation prompt
read -p "Are you sure you want to uninstall Optimal Scheduler? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "Uninstallation canceled."
    exit 0
fi

if [ -d "$INSTALL_DIR" ]; then
    echo "Removing installation directory..."
    rm -rf "$INSTALL_DIR"
else
    echo "Installation directory not found."
fi

if [ -f "$DESKTOP_FILE_PATH" ]; then
    echo "Removing .desktop file..."
    rm "$DESKTOP_FILE_PATH"
else
    echo ".desktop file not found."
fi

echo "Uninstallation complete."
