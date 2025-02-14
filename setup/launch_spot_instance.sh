#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

IAM_ROLE_ARN=$(yq e '.aws.iam_role_arn' $CONFIG_FILE)
IAM_INSTANCE_PROFILE=$(yq e '.aws.iam_instance_profile' $CONFIG_FILE)
REGION=$(yq e '.aws.region' $CONFIG_FILE)
AMI_ID=$(yq e '.ec2.ami_id' $CONFIG_FILE)
INSTANCE_TYPE=$(yq e '.ec2.instance_type' $CONFIG_FILE)
VOLUME_SIZE=$(yq e '.ec2.volume_size' $CONFIG_FILE)
USE_SPOT_INSTANCE=$(yq e '.ec2.use_spot_instance' $CONFIG_FILE)
KEY_PAIR_NAME=$(yq e '.aws.key_pair_name' $CONFIG_FILE)

# Launch EC2 instance with SSH key
if [[ "$USE_SPOT_INSTANCE" == "true" ]]; then
    echo "Requesting EC2 Spot Instance..."
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id "$AMI_ID" \
        --count 1 \
        --instance-type "$INSTANCE_TYPE" \
        --region "$REGION" \
        --iam-instance-profile Name="$IAM_INSTANCE_PROFILE" \
        --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE}}]" \
        --key-name "$KEY_PAIR_NAME" \
        --query 'Instances[0].InstanceId' --output text)
else
    echo "Launching EC2 On-Demand Instance..."
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id "$AMI_ID" \
        --count 1 \
        --instance-type "$INSTANCE_TYPE" \
        --region "$REGION" \
        --iam-instance-profile Name="$IAM_INSTANCE_PROFILE" \
        --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE}}]" \
        --key-name "$KEY_PAIR_NAME" \
        --query 'Instances[0].InstanceId' --output text)
fi

echo "EC2 Instance Launched: $INSTANCE_ID"
echo "$INSTANCE_ID" > instance_id.txt  # Save instance ID for later use
