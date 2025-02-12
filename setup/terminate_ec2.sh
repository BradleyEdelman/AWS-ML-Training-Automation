#!/bin/bash

# Load configuration
REGION=$(yq e '.aws.region' config.yaml)

# Retrieve instance ID
if [[ ! -f "instance_id.txt" ]]; then
    echo "Error: instance_id.txt not found. Did you launch an EC2 instance?"
    exit 1
fi
INSTANCE_ID=$(cat instance_id.txt)

# Confirm action
echo "Are you sure you want to terminate EC2 Instance ($INSTANCE_ID)? (yes/no)"
read RESPONSE

if [[ "$RESPONSE" == "yes" ]]; then
    aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region $REGION
    echo "Instance $INSTANCE_ID is being terminated..."
    rm -f instance_id.txt
else
    echo "Termination canceled."
fi
