#!/bin/bash

# Assume IAM Role
echo "Assuming IAM Role..."
bash setup/assume_iam_role.sh

# Launch Spot Instance
echo "Launching Spot Instance..."
bash setup/launch_spot_instance.sh

# Connect to Instance
echo "Connecting to EC2..."
bash setup/ssh_connect.sh

# Fetch Data
echo "Fetching Dataset..."
bash training/fetch_data.sh

# Validate Dataset Format
echo "Checking Data Format..."
python3 training/data_check_format.py

# Prepare Data for Model
echo "Preparing Data..."
python3 training/prepare_data.py

# Resume or Start Training
echo "Starting Training..."
bash training/start_training.sh

# Do more stuff I havent thought of yet
