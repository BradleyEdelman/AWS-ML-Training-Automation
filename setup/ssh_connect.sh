#!/bin/bash

# Load configuration
REGION=$(yq e '.aws.region' config.yaml)

# Retrieve instance ID
if [[ ! -f "instance_id.txt" ]]; then
    echo "Error: instance_id.txt not found. Did you launch an EC2 instance?"
    exit 1
fi
INSTANCE_ID=$(cat instance_id.txt)

# Get the public IP of the instance
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

if [[ "$PUBLIC_IP" == "None" ]]; then
    echo "Error: No public IP found. Ensure the instance is running."
    exit 1
fi

# SSH into instance
echo "Connecting to EC2 Instance at $PUBLIC_IP..."
ssh -i my-key.pem ubuntu@$PUBLIC_IP
