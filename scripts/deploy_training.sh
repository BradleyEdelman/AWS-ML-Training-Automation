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
bash training/data_fetch.sh

# Resume or Start Training
echo "Starting Training..."
bash training/train_model.py

# Do more stuff I havent thought of yet
