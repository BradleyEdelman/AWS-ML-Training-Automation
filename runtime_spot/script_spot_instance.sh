#!/bin/bash

# Installing shell requirements onto fresh Spot Instance
echo "Installing shell requirements..."
bash runtime_spot/08_install_requirements_spot.sh
sudo snap install yq

# Assume IAM Role on Spot Instance
echo "Assuming IAM Role..."
. runtime_spot/09_assume_iam_role_spot.sh

# Fetch Data
echo "Fetching Dataset..."
. runtime_spot/10_fetch_data.sh

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
source venv/bin/activate
python3 -m ml.train_model

# Sync logs to S3
echo "Syncing logs to S3..."
. runtime_spot/11_sync_log_to_s3.sh
