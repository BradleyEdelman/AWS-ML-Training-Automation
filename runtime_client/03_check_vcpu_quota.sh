#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' $CONFIG_FILE)

echo "Checking Spot Instance vCPU quota in region: $REGION..."

# Quota code for Spot vCPUs (change if needed)
SPOT_VCPU_QUOTA_CODE="L-34B43A08"

# Fetch the quota
QUOTA_OUTPUT=$(aws service-quotas get-service-quota \
	--service-code ec2 \
	--quota-code $SPOT_VCPU_QUOTA_CODE \
	--region "$REGION")

VCU_LIMIT=$(echo "$QUOTA_OUTPUT" | jq -r '.Quota.Value')

if [[ "$VCU_LIMIT" == "null" || -z "$VCU_LIMIT" ]]; then
	echo "Failed to retrieve vCPU quota. Check IAM permissions."
	exit 1
else
	echo "Current Spot vCPU limit: $VCU_LIMIT"
fi
