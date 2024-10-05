#!/bin/bash

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