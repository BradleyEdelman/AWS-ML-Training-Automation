#!/bin/bash

# Assume IAM Role
echo "Assuming IAM Role..."
. runtime_client/02_assume_iam_role_client.sh

# Check Spot Instance vCPU Quota
echo "Checking Spot Instance vCPU quota..."
. runtime_client/03_check_vcpu_quota.sh

# Launch Spot Instance
echo "Launching Spot Instance..."
. runtime_client/04_launch_spot_instance.sh

# Transfer files to Spot Instance
echo "Transferring files to Spot Instance..."
. runtime_client/05_transfer_files.sh

# Connect to Instance
echo "Connecting to EC2..."
. runtime_client/06_ssh_connect.sh
