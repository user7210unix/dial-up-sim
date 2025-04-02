#!/bin/bash

# Display info message
echo "====================================="
echo "Dial-Up Simulator Installer"
echo "You need to have the Chicago95 theme installed."
echo "====================================="

# Ask if you want to skip package installation
read -p "Do you want to skip installing dependencies? (y/n): " skip_install

# Clone the GitHub repository
echo "Cloning the dial-up simulator repository..."
git clone https://github.com/user7210unix/dial-up-sim.git

# Navigate to the cloned directory
cd dial-up-sim || exit

if [[ "$skip_install" != "y" && "$skip_install" != "Y" ]]; then
    echo "Installing dependencies..."

    # Install required packages
    if command -v apt > /dev/null 2>&1; then
        echo "Detected apt-based system (e.g., Ubuntu, Debian)"
        sudo apt update
        sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 dillo mpg123 python3-pip
        # Additional GStreamer packages for sound
        sudo apt install -y gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-ugly gstreamer1.0-libav
    elif command -v pacman > /dev/null 2>&1; then
        echo "Detected pacman-based system (e.g., Arch, Manjaro)"
        sudo pacman -Syu --noconfirm python-gobject gtk3 dillo mpg123 python-pip
        # Additional GStreamer packages for sound
        sudo pacman -S --noconfirm gstreamer gstreamer0.10-plugins gstreamer-plugins-good
    elif command -v dnf > /dev/null 2>&1; then
        echo "Detected dnf-based system (e.g., Fedora, CentOS)"
        sudo dnf install -y python3-gobject gtk3 dillo mpg123 python3-pip
        # Additional GStreamer packages for sound
        sudo dnf install -y gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-ugly gstreamer1-libav
    else
        echo "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi
fi

# Install pip packages if needed
echo "Installing Python dependencies..."
pip install --break-system-packages playsound

# Create necessary directories
echo "Setting up directories..."
sudo mkdir -p /usr/local/bin/dial-up-sim
sudo cp -r ./assets /usr/local/bin/dial-up-sim/assets
sudo cp modem-simulator.py /usr/local/bin/dial-up-sim/modem-simulator.py

# Make the script executable
echo "Making script executable..."
sudo chmod +x /usr/local/bin/dial-up-sim/modem-simulator.py

# Create a symlink to make it run with a shorter command
echo "Creating symlink..."
sudo ln -s /usr/local/bin/dial-up-sim/modem-simulator.py /usr/local/bin/modem-simulator

# Finish installation
echo "Installation complete! You can now run the dial-up simulator with the command:"
echo "modem-simulator"
echo "====================================="

