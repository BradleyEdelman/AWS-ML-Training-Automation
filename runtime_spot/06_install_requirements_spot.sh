#!/bin/bash

echo "Starting Spot Instance setup..."

# 1️.1 Install shell dependencies
echo "Installing shell dependencies..."
sudo apt-get update -y

# Fix Windows carriage return thing
sed -i 's/\r$//' requirements/requirements-sh.txt

# Install shell dependencies via APT or Snap (yq has issues)
while IFS= read -r package; do
    package=$(echo "$package" | tr -d '\r') 
    if [[ -z "$package" ]]; then
        continue
    fi

    echo "Installing $package via APT..."
    if ! sudo apt-get install -y "$package"; then
        echo "APT install failed for $package, trying Snap..."
        sudo snap install "$package" || echo "Failed to install $package"
    fi
done < requirements/requirements-sh.txt

echo "Shell dependencies installed."

# Disable needrestart prompts
export NEEDRESTART_MODE=a
export NEEDRESTART_SUSPEND=1



# 2. Expand Spot Storage
echo "Checking and expanding available storage..."

# Identify root partition dynamically
DEVICE=$(lsblk -o NAME,MOUNTPOINT | awk '$2 == "/" {print "/dev/" $1}' | head -n 1)
EBS_VOLUME=$(lsblk -o NAME | grep nvme1n1 | head -n 1)  # Detect XGB EBS volume

if [[ -z "$EBS_VOLUME" ]]; then
    echo "ERROR: No additional EBS volume found. Skipping expansion."
else
    echo "Detected additional volume: /dev/$EBS_VOLUME"
    sudo file -s /dev/$EBS_VOLUME | grep -q "data" && sudo mkfs -t ext4 /dev/$EBS_VOLUME
    sudo mkdir -p /mnt/data
    sudo mount /dev/$EBS_VOLUME /mnt/data
    echo "/dev/$EBS_VOLUME /mnt/data ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
    echo "Storage expansion complete!"
fi

# Verify new space
df -h



# 3. Install AWS CLI

# Ensure unzip is installed before AWS CLI setup
if ! command -v unzip &> /dev/null; then
    echo "Installing unzip..."
    sudo apt-get install -y unzip
fi

if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
    echo "AWS CLI installed successfully."
else
    echo "AWS CLI already installed."
fi



# 4. Install Python and dependencies
echo "Setting up Python environment..."
sudo apt-get install -y python3 python3-pip python3-venv

# Create venv
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
fi
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements/requirements.txt

echo "Python dependencies installed."

echo "Spot Instance setup complete!"
