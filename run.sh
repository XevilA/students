#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo dnf update -y

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo dnf install -y python3 python3-pip

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip3 install --upgrade pip

# Install Python packages
echo "Installing Python packages: ttkbootstrap, opencv-python, cmake, dlib, face_recognition..."
pip3 install ttkbootstrap opencv-python cmake dlib face_recognition

# Install Visual Studio Code
echo "Adding Visual Studio Code repository..."
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

echo "Installing Visual Studio Code..."
sudo dnf check-update
sudo dnf install -y code

# Install Google Chrome
echo "Adding Google Chrome repository..."
sudo dnf config-manager --set-enabled google-chrome

echo "Installing Google Chrome..."
sudo dnf install -y google-chrome-stable

# Set execute permission for the script (itself)
echo "Setting execute permissions for the script..."
sudo chmod +x run.sh

# Confirm installations
echo "Installation complete. Verifying installations..."

# Verify Python and pip
python3 --version
pip3 --version

# Check installed Python packages
pip3 list | grep -E "ttkbootstrap|opencv-python|cmake|dlib|face_recognition"

# Verify Visual Studio Code and Google Chrome
code --version
google-chrome --version

echo "All done!"