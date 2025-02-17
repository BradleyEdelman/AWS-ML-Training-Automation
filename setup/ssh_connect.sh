#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' $CONFIG_FILE)

# Retrieve instance ID
if [[ ! -f "setup/instance_id.txt" ]]; then
    echo "Error: instance_id.txt not found. Did you launch an EC2 instance?"
    exit 1
fi
INSTANCE_ID=$(cat setup/instance_id.txt)

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

# Get the security group ID
SECURITY_GROUP_ID=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
    --output text)

# Check if SSH is already open
SSH_RULE_EXISTS=$(aws ec2 describe-security-groups \
    --group-ids $SECURITY_GROUP_ID \
    --region $REGION \
    --query "SecurityGroups[0].IpPermissions[?FromPort==\`22\` && IpRanges[?CidrIp=='0.0.0.0/0']].FromPort" \
    --output text)

if [[ -z "$SSH_RULE_EXISTS" ]]; then
    echo "Adding SSH (port 22) access to security group $SECURITY_GROUP_ID..."
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp --port 22 --cidr 0.0.0.0/0 \
        --region $REGION
    echo "SSH access enabled!"
else
    echo "SSH access already enabled!"
fi

# SSH into instance
echo "Connecting to EC2 Instance at $PUBLIC_IP..."
ssh -i setup/ec2-training-key.pem ubuntu@$PUBLIC_IP
