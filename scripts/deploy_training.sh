#!/bin/bash

# Assume IAM Role
echo "Assuming IAM Role..."
bash runtime/02_assume_iam_role.sh

# Launch Spot Instance
echo "Launching Spot Instance..."
bash runtime/03_launch_spot_instance.sh

# Connect to Instance
echo "Connecting to EC2..."
bash runtime/04_ssh_connect.sh

# Fetch Data
echo "Fetching Dataset..."
bash runtime/05_data_fetch.sh

# Resume or Start Training
echo "Starting Training..."
bash training/train_model.py

# Do more stuff I havent thought of yet
