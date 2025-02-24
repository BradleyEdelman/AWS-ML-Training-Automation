#!/bin/bash

# Installing shell requirements onto fresh Spot Instance
echo "Installing shell requirements..."
bash runtime_spot/06_install_requirements_spot.sh

# Assume IAM Role on Spot Instance
echo "Assuming IAM Role..."
. runtime_spot/07_assume_iam_role_spot.sh

# Fetch Data
echo "Fetching Dataset..."
. runtime_spot/08_fetch_data.sh

# Resume or Start Training
echo "Starting Training..."
cd ml
python3 train_model.py
