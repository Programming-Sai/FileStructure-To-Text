#!/bin/bash

# Define the installation directory
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="ftt"
PYTHON_SCRIPT_PATH="$(pwd)/main.py"

# Check if the script is being run with sudo or as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root or with sudo"
  exit 1
fi

# Verify the Python script exists
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
  echo "Python script not found at $PYTHON_SCRIPT_PATH"
  exit 1
fi

# Copy the Python script to a standard location
cp "$PYTHON_SCRIPT_PATH" "$INSTALL_DIR/$SCRIPT_NAME.py"
if [ $? -ne 0 ]; then
  echo "Failed to copy Python script to $INSTALL_DIR"
  exit 1
fi

# Create the executable script in /usr/local/bin
cat <<EOL > "$INSTALL_DIR/$SCRIPT_NAME"
#!/bin/bash
python3 $INSTALL_DIR/$SCRIPT_NAME.py "\$@"
EOL

# Make the script executable
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
if [ $? -ne 0 ]; then
  echo "Failed to make $INSTALL_DIR/$SCRIPT_NAME executable"
  exit 1
fi

# Create the uninstall script in /usr/local/bin
cat <<EOL > "$INSTALL_DIR/uninstall.sh"
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

if [ -f "$INSTALL_DIR/uninstall.sh" ]; then
    rm "$INSTALL_DIR/uninstall.sh"
fi

echo "$SCRIPT_NAME command uninstalled successfully!"
EOL

# Make the uninstall script executable
chmod +x "$INSTALL_DIR/uninstall.sh"
if [ $? -ne 0 ]; then
  echo "Failed to make $INSTALL_DIR/uninstall.sh executable"
  exit 1
fi

# Verify installation
if command -v $SCRIPT_NAME &> /dev/null
then
    echo "$SCRIPT_NAME command installed successfully!"
else
    echo "Failed to install $SCRIPT_NAME command."
fi
