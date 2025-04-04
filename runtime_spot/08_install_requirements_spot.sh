#!/bin/bash

echo "Starting Spot Instance setup..."

# 1. Install shell dependencies
export DEBIAN_FRONTEND=noninteractive # No user prompts

echo "Updating package lists..."
sudo apt-get update -y -q

# Install `yq` specifically using Snap
echo "Installing yq via Snap..."
sudo snap install yq || echo "Failed to install yq"

# Install shell dependencies via APT (except yq, which is installed via Snap)
echo "Installing shell dependencies..."
while IFS= read -r package; do
	package=$(echo "$package" | tr -d '\r') # Remove Windows carriage return
	if [[ -z "$package" || "$package" == "yq" ]]; then
		continue # Skip empty lines and yq (installed separately)
	fi

	echo "Installing $package..."
	sudo apt-get install -y -q "$package"
done <requirements/requirements-sh.txt

echo "All shell dependencies installed."

# Disable needrestart prompts
export NEEDRESTART_MODE=a
export NEEDRESTART_SUSPEND=1

# 2. Expand Spot storage to match config.yaml
echo "Expanding EBS storage to config specifications..."

# Identify root partition
EBS_VOLUME=$(lsblk -o NAME | grep nvme1n1 | head -n 1) # Detect attached EBS volume

if [[ -z "$EBS_VOLUME" ]]; then
	echo "ERROR: No additional EBS volume found. Skipping expansion."
else
	echo "Detected additional volume: /dev/$EBS_VOLUME"
	sudo file -s /dev/"$EBS_VOLUME" | grep -q "data" && sudo mkfs -t ext4 /dev/"$EBS_VOLUME"
	sudo mkdir -p /mnt/data
	sudo mount /dev/"$EBS_VOLUME" /mnt/data
	echo "/dev/$EBS_VOLUME /mnt/data ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
	echo "Storage expansion complete!"
fi

# Verify disk space
df -h

# 3. Install AWS CLI
echo "Checking for AWS CLI..."

if ! command -v aws &>/dev/null; then
	echo "Installing AWS CLI..."
	curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	unzip -q awscliv2.zip
	sudo ./aws/install
	rm -rf aws awscliv2.zip
	echo "AWS CLI installed successfully."
else
	echo "AWS CLI already installed."
fi

# 4. Install Python and dependencies
echo "Setting up Python environment..."
sudo apt-get install -y -q python3 python3-pip python3-venv

# Define the venv directory
VENV_DIR="$HOME/venv"

# Create virtual environment in a persistent location
if [[ ! -d "$VENV_DIR" ]]; then
	python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

pip install --upgrade pip -q
pip install -r requirements/requirements.txt -q

echo "Python dependencies installed."

echo "Spot Instance setup complete!"
