#!/bin/bash

# Install Chocolatey (if not already there)
if ! command -v choco &> /dev/null; then
    echo "Installing Chocolatey..."
    powershell -NoProfile -ExecutionPolicy Bypass -Command \
        "Set-ExecutionPolicy Bypass -Scope Process -Force; \
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    export PATH="$PATH:/c/ProgramData/chocolatey/bin"
fi

# Install dependecnies
while IFS= read -r package; do
    if ! command -v "$package" &> /dev/null; then
        echo "Installing $package..."
        choco install "$package" -y
    else
        echo "$package is already installed."
    fi
done < requirements/requirements_sh.txt

echo "All dependencies installed. Restart Git Bash to ensure changes take effect."
