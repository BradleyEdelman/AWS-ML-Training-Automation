#!/bin/bash

# Load configuration
REGION=$(yq e '.aws.region' config.yaml)

# Retrieve instance ID
if [[ ! -f "instance_id.txt" ]]; then
    echo "Error: instance_id.txt not found. Did you launch an EC2 instance?"
    exit 1
fi
INSTANCE_ID=$(cat instance_id.txt)

# Get instance status
INSTANCE_STATE=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].State.Name' \
    --output text)

echo "EC2 Instance ($INSTANCE_ID) is currently: $INSTANCE_STATE"
