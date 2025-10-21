#!/bin/bash
# ==============================================
# StormShield Installer (Universal Linux + Auto-Service)
# Author: Sylias Shufelt
# Purpose: Install dependencies, set permissions,
#          and automatically create + start systemd service.
# ==============================================

set -e

# Detect Linux distro
echo "[Install] Detecting Linux distribution..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "[Install] Cannot detect Linux distribution. Exiting."
    exit 1
fi

# Install system packages per distro
install_packages_debian() {
    sudo apt update || true
    sudo apt install -y python3 python3-pip python3-venv curl || true
}

install_packages_arch() {
    sudo pacman -Sy --noconfirm python python-pip python-psutil curl || true
}

install_packages_fedora() {
    sudo dnf install -y python3 python3-pip python3-psutil curl || true
}

install_packages_centos() {
    sudo yum install -y epel-release
    sudo yum install -y python3 python3-pip python3-psutil curl || true
}

echo "[Install] Installing Python and dependencies for $DISTRO..."
case "$DISTRO" in
    ubuntu|debian)
        install_packages_debian
        ;;
    arch)
        install_packages_arch
        ;;
    fedora)
        install_packages_fedora
        ;;
    centos|rhel)
        install_packages_centos
        ;;
    *)
        echo "[Install] Distribution $DISTRO not fully supported. Attempting pip only."
        ;;
esac

# Install Python dependencies
echo "[Install] Installing Python packages via pip..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Set script permissions
echo "[Install] Setting executable permissions for scripts..."
chmod +x src/*.py

# Create systemd service
SERVICE_FILE="/etc/systemd/system/stormshield.service"
CURRENT_DIR=$(pwd)
CURRENT_USER=$(whoami)

echo "[Install] Creating systemd service at $SERVICE_FILE..."
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=StormShield – Home Server Storm Protection
After=network.target

[Service]
Type=simple
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 $CURRENT_DIR/src/stormshield.py
Restart=on-failure
User=$CURRENT_USER

[Install]
WantedBy=multi-user.target
EOL

# Enable and start the service
echo "[Install] Enabling and starting StormShield service..."
sudo systemctl daemon-reload
sudo systemctl enable stormshield.service
sudo systemctl start stormshield.service

echo "[Install] Installation complete! ✅"
echo "StormShield is now running as a systemd service."
echo "Check logs with: journalctl -u stormshield.service -f"
