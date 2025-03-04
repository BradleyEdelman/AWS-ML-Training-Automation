#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
IAM_ROLE_ARN=$(yq e '.aws.iam_role_arn' $CONFIG_FILE)
SESSION_NAME=$(yq e '.aws.session_name' $CONFIG_FILE)
PROFILE_NAME=$(yq e '.aws.cli_profile' $CONFIG_FILE)

# User correct AWS CLI profile
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_PROFILE
export AWS_PROFILE=$PROFILE_NAME

# Assume the IAM Role
echo "Assuming IAM Role: $IAM_ROLE_ARN..."
CREDENTIALS=$(aws sts assume-role --role-arn "$IAM_ROLE_ARN" --role-session-name "$SESSION_NAME" --query 'Credentials' --output json --profile "$PROFILE_NAME" 2>/dev/null) &&
	AWS_ACCESS_KEY_ID=$(echo "$CREDENTIALS" | jq -r '.AccessKeyId') &&
	export AWS_ACCESS_KEY_ID &&
	AWS_SECRET_ACCESS_KEY=$(echo "$CREDENTIALS" | jq -r '.SecretAccessKey') &&
	export AWS_SECRET_ACCESS_KEY &&
	AWS_SESSION_TOKEN=$(echo "$CREDENTIALS" | jq -r '.SessionToken') &&
	export AWS_SESSION_TOKEN

# Verify if the assumed role is correct
ASSUMED_ROLE_ARN=$(aws sts get-caller-identity --query "Arn" --output text 2>/dev/null)

if [[ "$ASSUMED_ROLE_ARN" == *":assumed-role/"* ]]; then
	echo "Successfully assumed IAM role: $ASSUMED_ROLE_ARN"
else
	echo "ERROR: Assumed role verification failed! Expected: $IAM_ROLE_ARN, but got: $ASSUMED_ROLE_ARN"
	exit 1
fi
