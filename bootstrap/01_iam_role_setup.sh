#!/bin/bash

# Configuration variables
AWS_REGION="eu-central-1"
IAM_ROLE_NAME="EC2-Training-Role"
IAM_INSTANCE_PROFILE="EC2-Training-Instance-Profile"

# Select IAM policy type
echo "Choose IAM policy level: (1) Restricted (2) Full Access"
read -p "Enter 1 or 2: " POLICY_CHOICE

if [[ "$POLICY_CHOICE" == "1" ]]; then
    PERMISSIONS_POLICY="iam_policies/iam_permissions_restricted.json"
elif [[ "$POLICY_CHOICE" == "2" ]]; then
    PERMISSIONS_POLICY="iam_policies/iam_permissions_full.json"
else
    echo "Invalid choice. Exiting."
    exit 1
fi

TRUST_POLICY="iam_policies/iam_trust_policy.json"

echo "Creating IAM Role: $IAM_ROLE_NAME..."
aws iam create-role --role-name "$IAM_ROLE_NAME" --assume-role-policy-document file://$TRUST_POLICY

echo "Attaching Policy to IAM Role..."
aws iam put-role-policy --role-name "$IAM_ROLE_NAME" --policy-name "EC2-Training-Policy" --policy-document file://$PERMISSIONS_POLICY

echo "Creating IAM Instance Profile: $IAM_INSTANCE_PROFILE..."
aws iam create-instance-profile --instance-profile-name "$IAM_INSTANCE_PROFILE"

echo "Adding Role to Instance Profile..."
aws iam add-role-to-instance-profile --instance-profile-name "$IAM_INSTANCE_PROFILE" --role-name "$IAM_ROLE_NAME"

echo "IAM Role & Profile setup complete!"
