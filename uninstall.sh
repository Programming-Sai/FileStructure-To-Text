#!/bin/bash

# Define the installation directory
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="ftt"

# Remove the Python script and the executable script if they exist
if [ -f "$INSTALL_DIR/$SCRIPT_NAME.py" ]; then
    rm "$INSTALL_DIR/$SCRIPT_NAME.py"
fi

if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ]; then
    rm "$INSTALL_DIR/$SCRIPT_NAME"
fi

echo "$SCRIPT_NAME command uninstalled successfully!"
