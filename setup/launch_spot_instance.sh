#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

# Extract values from config.yaml using yq (YAML processor)
IAM_ROLE_ARN=$(yq e '.aws.iam_role_arn' $CONFIG_FILE)
REGION=$(yq e '.aws.region' $CONFIG_FILE)
INSTANCE_TYPE=$(yq e '.ec2.instance_type' $CONFIG_FILE)
VOLUME_SIZE=$(yq e '.ec2.volume_size' $CONFIG_FILE)
USE_SPOT_INSTANCE=$(yq e '.ec2.use_spot_instance' $CONFIG_FILE)

# Amazon Machine Image (AMI) - Choose Deep Learning AMI
AMI_ID="ami-xxxxxxxxxxxxx"  # Replace with your Deep Learning AMI

# Launch EC2 instance
if [[ "$USE_SPOT_INSTANCE" == "true" ]]; then
    echo "Requesting EC2 Spot Instance..."
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id $AMI_ID \
        --count 1 \
        --instance-type $INSTANCE_TYPE \
        --region $REGION \
        --iam-instance-profile Name=$IAM_ROLE_ARN \
        --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE}}]" \
        --query 'Instances[0].InstanceId' --output text)
else
    echo "Launching EC2 On-Demand Instance..."
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id $AMI_ID \
        --count 1 \
        --instance-type $INSTANCE_TYPE \
        --region $REGION \
        --iam-instance-profile Name=$IAM_ROLE_ARN \
        --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE}}]" \
        --query 'Instances[0].InstanceId' --output text)
fi

echo "EC2 Instance Launched: $INSTANCE_ID"
echo $INSTANCE_ID > instance_id.txt  # Save instance ID for later use
