#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
IAM_ROLE_ARN=$(yq e '.aws.iam_role_arn' "$CONFIG_FILE")
SESSION_NAME="Spot-Instance-Session"
PROFILE_NAME=$(yq e '.aws.cli_profile' "$CONFIG_FILE")
AWS_REGION=$(yq e '.aws.region' "$CONFIG_FILE")

# Remove existing AWS CLI profile to avoid duplicates
echo "Cleaning up AWS CLI profile ($PROFILE_NAME) to avoid duplicates..."
if aws configure list-profiles | grep -q "$PROFILE_NAME"; then
    aws configure set region "" --profile "$PROFILE_NAME"
    aws configure set output "" --profile "$PROFILE_NAME"
    sed -i "/\[profile $PROFILE_NAME\]/,/^$/d" ~/.aws/config
    sed -i "/\[$PROFILE_NAME\]/,/^$/d" ~/.aws/credentials
fi

# Set AWS CLI profile from scratch
echo "Setting AWS CLI profile ($PROFILE_NAME)..."
aws configure set region "$AWS_REGION" --profile "$PROFILE_NAME"
aws configure set output json --profile "$PROFILE_NAME"

# Clear previous AWS session variables
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_PROFILE
export AWS_PROFILE="$PROFILE_NAME"

# Assume the IAM Role
echo "Assuming IAM Role inside AWS Spot Instance..."
CREDENTIALS=$(aws sts assume-role --role-arn "$IAM_ROLE_ARN" --role-session-name "$SESSION_NAME" --query 'Credentials' --output json --profile "$PROFILE_NAME")

if [[ -z "$CREDENTIALS" || "$CREDENTIALS" == "null" ]]; then
    echo "ERROR: Failed to assume IAM role. Check IAM permissions."
    exit 1
fi

# Extract credentials and set environment variables
export AWS_ACCESS_KEY_ID=$(echo "$CREDENTIALS" | jq -r '.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo "$CREDENTIALS" | jq -r '.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo "$CREDENTIALS" | jq -r '.SessionToken')

# Verify assumed role
ASSUMED_ROLE_ARN=$(aws sts get-caller-identity --query "Arn" --output text)

if [[ "$ASSUMED_ROLE_ARN" == *":assumed-role/"* ]]; then
    echo "Successfully assumed IAM role: $ASSUMED_ROLE_ARN"
else
    echo "ERROR: Assumed role verification failed! Expected: $IAM_ROLE_ARN, but got: $ASSUMED_ROLE_ARN"
    exit 1
fi
