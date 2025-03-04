#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' $CONFIG_FILE)

INSTANCE_ID=$(cat instance_id.txt)

echo "Monitoring AWS Spot Termination Notices for Instance: $INSTANCE_ID..."

while true; do
	TERMINATION_NOTICE=$(aws ec2 describe-instance-status \
		--instance-ids "$INSTANCE_ID" \
		--region "$REGION" \
		--query "InstanceStatuses[0].Events[?Code==$(instance-stop)].NotBefore" \
		--output text)

	if [[ "$TERMINATION_NOTICE" != "None" && -n "$TERMINATION_NOTICE" ]]; then
		echo "AWS Spot Termination Notice Received!"

		# Save checkpoint
		echo "Saving model checkpoint..."
		python3 training/checkpoint_save.py

		# Stop training by creating a shutdown flag
		echo "Stopping model training..."
		touch training/STOP_TRAINING_FLAG

		echo "Cleanup complete. Preparing for shutdown..."
		exit 0
	fi

	sleep 5
done
