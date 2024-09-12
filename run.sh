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

# Confirm installations
echo "Installation complete. Verifying installations..."
python3 --version
pip3 --version
pip3 list | grep -E "ttkbootstrap|opencv-python|cmake|dlib|face_recognition"

echo "All done!"