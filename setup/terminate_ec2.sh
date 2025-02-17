#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' $CONFIG_FILE)

# Retrieve instance ID
if [[ ! -f "setup/instance_id.txt" ]]; then
    echo "Error: setup/instance_id.txt not found. Did you launch an EC2 instance?"
    exit 1
fi
INSTANCE_ID=$(cat setup/instance_id.txt)

# Check if instance is already terminated
INSTANCE_STATE=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query 'Reservations[0].Instances[0].State.Name' \
    --output text)

if [[ "$INSTANCE_STATE" == "terminated" ]]; then
    echo "Instance $INSTANCE_ID is already terminated."
    rm -f setup/instance_id.txt
    exit 0
fi

# Confirm action
echo "Are you sure you want to terminate EC2 Instance ($INSTANCE_ID)? (yes/no)"
read RESPONSE

if [[ "$RESPONSE" == "yes" ]]; then
    aws ec2 terminate-instances --instance-ids "$INSTANCE_ID" --region "$REGION"
    echo "Instance $INSTANCE_ID is being terminated..."
    
    # Wait for termination to complete
    aws ec2 wait instance-terminated --instance-ids "$INSTANCE_ID" --region "$REGION"
    
    echo "Instance $INSTANCE_ID terminated successfully!"
    
    # Clean up files
    rm -f setup/instance_id.txt
    
    # Optional: Delete SSH key pair if instance is permanently gone
    KEY_PAIR_NAME=$(yq e '.ec2.key_pair_name' "$CONFIG_FILE")
    echo "Deleting key pair '$KEY_PAIR_NAME' from AWS..."
    aws ec2 delete-key-pair --key-name "$KEY_PAIR_NAME" --region "$REGION"
    
    # Remove local .pem key file
    if [[ -f "setup/$KEY_PAIR_NAME.pem" ]]; then
        echo "Removing local key file: setup/$KEY_PAIR_NAME.pem"
        rm -f "setup/$KEY_PAIR_NAME.pem"
    fi

    echo "Cleanup complete!"
else
    echo "Termination canceled."
fi
