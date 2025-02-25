#!/bin/bash

# Installing shell requirements onto fresh Spot Instance
echo "Installing shell requirements..."
bash runtime_spot/06_install_requirements_spot.sh

# Convert a few scripts from Windows to Unix
dos2unix config.yaml
dos2unix runtime_spot/07_assume_iam_role_spot.sh

# Assume IAM Role on Spot Instance
echo "Assuming IAM Role..."
. runtime_spot/07_assume_iam_role_spot.sh

# Fetch Data
echo "Fetching Dataset..."
. runtime_spot/08_fetch_data.sh

# Activate virtual environment before training
VENV_DIR="$HOME/venv"
if [[ -d "$VENV_DIR" ]]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "ERROR: Virtual environment not found at $VENV_DIR"
    exit 1
fi

# Resume or Start Training
echo "Starting Training..."
cd ml
python3 train_model.py
