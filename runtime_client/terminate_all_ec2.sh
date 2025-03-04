#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
AWS_REGION=$(yq e '.aws.region' $CONFIG_FILE)

# Define the tag key and value
TAG_KEY="CreatedBy"
TAG_VALUE="EC2-Training-Role"

echo "Searching for EC2 instances with tag $TAG_KEY=$TAG_VALUE in region $AWS_REGION..."

# Get all running instances with this tag
INSTANCE_IDS=$(aws ec2 describe-instances \
	--region "$AWS_REGION" \
	--filters "Name=tag:$TAG_KEY,Values=$TAG_VALUE" "Name=instance-state-name,Values=running" \
	--query "Reservations[].Instances[].InstanceId" \
	--output text)

# Check if we found any instances
if [[ -z "$INSTANCE_IDS" || "$INSTANCE_IDS" == "None" ]]; then
	echo "No instances found with tag $TAG_KEY=$TAG_VALUE."
	exit 0
fi

# Terminate instances
echo "Terminating instances: $INSTANCE_IDS..."
aws ec2 terminate-instances --region "$AWS_REGION" --instance-ids "$INSTANCE_IDS"

echo "Termination command sent. Checking status..."

# Wait for termination to complete
aws ec2 wait instance-terminated --region "$AWS_REGION" --instance-ids "$INSTANCE_IDS"

echo "All tagged instances ($TAG_VALUE) have been terminated successfully."
