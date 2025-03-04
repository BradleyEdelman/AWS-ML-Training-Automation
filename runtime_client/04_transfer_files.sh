#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

REGION=$(yq e '.aws.region' $CONFIG_FILE)
INSTANCE_ID=$(cat runtime_client/instance_id.txt)
KEY_PAIR_NAME=$(yq e '.ec2.key_pair_name' $CONFIG_FILE)
KEY_FILE_PATH="runtime_client/$KEY_PAIR_NAME.pem"

# Get the public IP of the instance
PUBLIC_IP=$(aws ec2 describe-instances \
	--instance-ids "$INSTANCE_ID" \
	--region "$REGION" \
	--query 'Reservations[0].Instances[0].PublicIpAddress' \
	--output text)

if [[ "$PUBLIC_IP" == "None" || -z "$PUBLIC_IP" ]]; then
	echo "Error: No public IP found. Ensure the instance is running."
	exit 1
fi

# Ensure SSH key exists
if [[ ! -f "$KEY_FILE_PATH" ]]; then
	echo "Error: SSH key file not found: $KEY_FILE_PATH"
	exit 1
fi

# # Automatically accept SSH host key and install dos2nix on Spot Instance
# ssh -o "StrictHostKeyChecking=no" -i "$KEY_FILE_PATH" ubuntu@"$PUBLIC_IP" <<'EOF'
# sudo apt-get update -y && sudo apt-get install -y dos2unix
# EOF

# Transfer files to EC2 instance
echo "Transferring files to EC2 instance ($PUBLIC_IP)..."

ssh -i "$KEY_FILE_PATH" ubuntu@"$PUBLIC_IP" "mkdir -p ~/{requirements,ml,runtime_spot}"

scp -i "$KEY_FILE_PATH" -r requirements ubuntu@"$PUBLIC_IP":~/
scp -i "$KEY_FILE_PATH" -r ml ubuntu@"$PUBLIC_IP":~/
scp -i "$KEY_FILE_PATH" -r runtime_spot ubuntu@"$PUBLIC_IP":~/
scp -i "$KEY_FILE_PATH" -r config*.yaml ubuntu@"$PUBLIC_IP":~/
scp -i "$KEY_FILE_PATH" -r runtime_client/instance_id.txt ubuntu@"$PUBLIC_IP":~/

# # Convert transferred files to Unix format
# ssh -i "$KEY_FILE_PATH" ubuntu@"$PUBLIC_IP" <<'EOF'
# "find ~ -type f \( -name '*.sh' -o -name '*.yaml' -o -name '*.txt' \) -exec dos2unix {} \;"
# EOF

echo "Files successfully transferred!"
