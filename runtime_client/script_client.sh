#!/bin/bash

# Assume IAM Role
echo "Assuming IAM Role..."
. runtime_client/02_assume_iam_role_client.sh

# Launch Spot Instance
echo "Launching Spot Instance..."
. runtime_client/03_launch_spot_instance.sh

# Transfer files to Spot Instance
echo "Transferring files to Spot Instance..."
. runtime_client/04_transfer_files.sh

# Connect to Instance
echo "Connecting to EC2..."
. runtime_client/05_ssh_connect.sh
