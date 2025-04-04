#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

IAM_INSTANCE_PROFILE=$(yq e '.aws.iam_instance_profile' $CONFIG_FILE)
REGION=$(yq e '.aws.region' $CONFIG_FILE)
AMI_ID=$(yq e '.ec2.ami_id' $CONFIG_FILE)
INSTANCE_TYPE=$(yq e '.ec2.instance_type' $CONFIG_FILE)
VOLUME_SIZE=$(yq e '.ec2.volume_size' $CONFIG_FILE)
# USE_SPOT_INSTANCE=$(yq e '.ec2.use_spot_instance' $CONFIG_FILE)

KEY_PAIR_NAME=$(yq e '.ec2.key_pair_name' $CONFIG_FILE)
KEY_FILE_PATH="runtime_client/$KEY_PAIR_NAME.pem"

# Check if key pair exists
echo "Checking if key pair '$KEY_PAIR_NAME' exists..."
EXISTING_KEY=$(aws ec2 describe-key-pairs --key-names "$KEY_PAIR_NAME" --region "$REGION" --query 'KeyPairs[0].KeyName' --output text 2>/dev/null)

# In case you delete the .pem file accidentally (which i've done)
if [[ "$EXISTING_KEY" == "None" || -z "$EXISTING_KEY" || ! -f "$KEY_FILE_PATH" ]]; then
	echo "Key pair or .pem file missing. Recreating key pair..."

	# Delete existing key pair (if it still exists without .pem file)
	if [[ -n "$EXISTING_KEY" ]]; then
		aws ec2 delete-key-pair --key-name "$KEY_PAIR_NAME" --region "$REGION"
		echo "Deleted old key pair: $KEY_PAIR_NAME"
	fi

	# Create new key pair
	aws ec2 create-key-pair --key-name "$KEY_PAIR_NAME" --region "$REGION" --query "KeyMaterial" --output text >"$KEY_FILE_PATH"
	chmod 400 "$KEY_FILE_PATH"
	echo "New key pair created and saved as $KEY_FILE_PATH"
else
	echo "Key pair '$KEY_PAIR_NAME' already exists."
fi

# Get security group ID
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values="default" --region "$REGION" --query "SecurityGroups[0].GroupId" --output text)

# Open SSH if not allowed
SSH_RULE_EXISTS=$(aws ec2 describe-security-groups --group-ids "$SECURITY_GROUP_ID" --region "$REGION" --query "SecurityGroups[0].IpPermissions[?ToPort==$(22)].IpRanges[?CidrIp==$(0.0.0.0/0)]" --output text)
if [[ -z "$SSH_RULE_EXISTS" ]]; then
	echo "Adding SSH rule to security group..."
	aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
	echo "SSH access enabled."
fi

# Launch EC2 instance
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

echo "EC2 Instance Launched: $INSTANCE_ID"
echo "$INSTANCE_ID" >runtime_client/instance_id.txt # Save instance ID for later
