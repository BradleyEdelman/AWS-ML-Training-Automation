#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' $CONFIG_FILE)

INSTANCE_ID=$(cat runtime_client/instance_id.txt)

# Check if instance is already terminated
INSTANCE_STATE=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query 'Reservations[0].Instances[0].State.Name' \
    --output text)

if [[ "$INSTANCE_STATE" == "terminated" ]]; then
    echo "Instance $INSTANCE_ID is already terminated."
    rm -f runtime_client/instance_id.txt
    exit 0
fi

aws ec2 terminate-instances --instance-ids "$INSTANCE_ID" --region "$REGION"
echo "Instance $INSTANCE_ID is being terminated..."

# Wait for termination to complete
aws ec2 wait instance-terminated --instance-ids "$INSTANCE_ID" --region "$REGION"
echo "Instance $INSTANCE_ID terminated successfully!"

# Clean up files
rm -f runtime_client/instance_id.txt

# Delete SSH key pair
KEY_PAIR_NAME=$(yq e '.ec2.key_pair_name' "$CONFIG_FILE")
echo "Deleting key pair '$KEY_PAIR_NAME' from AWS..."
aws ec2 delete-key-pair --key-name "$KEY_PAIR_NAME" --region "$REGION"

# Remove local .pem key file
if [[ -f "runtime_client/$KEY_PAIR_NAME.pem" ]]; then
    echo "Removing local key file: runtime_client/$KEY_PAIR_NAME.pem"
    rm -f "runtime_client/$KEY_PAIR_NAME.pem"
fi

echo "Cleanup complete!"
