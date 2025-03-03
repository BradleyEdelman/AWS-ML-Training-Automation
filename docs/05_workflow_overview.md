# Workflow Overview Guide

This document provides an explanation of the general overview of how ML training can be automatically delpoyed on an EC2 Spot Instance. This procedue is broken into two majors steps based on what is needed on the local client machine and on the SSH'd EC2 Spot Instance. 

1️. **`script_client.sh`** (Run from your local machine)  
2️. **`script_spot_instance.sh`** (Runs inside the AWS Spot Instance)  

Here is further information about what each of these scripts does. Further details about each step can be found in the linked script.
---

### **Client-Side Workflow: [`script_client.sh`](runtime_client/script_client.sh)**
| **Step**                | **Script** | **Description** |
|-------------------------|-----------|----------------|
| **1. Assume IAM Role** | [`02_assume_iam_role_client.sh`](runtime_client/02_assume_iam_role_client.sh) | Assumes AWS IAM role for authentication |
| **2. Launch Spot Instance** | [`03_launch_spot_instance.sh`](runtime_client/03_launch_spot_instance.sh) | Requests a new AWS Spot Instance |
| **3. Transfer Files** | [`04_transfer_files.sh`](runtime_client/04_transfer_files.sh) | Copies scripts, and configs to Spot Instance |
| **4. SSH into Instance** | [`05_ssh_connect.sh`](runtime_client/05_ssh_connect.sh) | Connects to Spot Instance |

---

### **Spot Instance Workflow [`script_spot_instance.sh`](runtime_spot/script_spot_instance.sh)**
| **Step**                | **Script** | **Description** |
|-------------------------|-----------|----------------|
| **5. Install Dependencies** | [`06_install_requirements_spot.sh`](runtime_spot/06_install_requirements_spot.sh) | Installs Python and shell dependencies |
| **6. Assume IAM Role (on Spot)** | [`07_assume_iam_role_spot.sh`](runtime_spot/07_assume_iam_role_spot.sh) | Ensures Spot Instance has proper AWS permissions |
| **7. Fetch Data from S3** | [`08_fetch_data.sh`](runtime_spot/08_fetch_data.sh) | Downloads dataset and previous training checkpoints from S3 |
| **8. Start Training** | [`train_model.py`](ml/train_model.py) | Runs ML training |
| **9. Detect Spot Termination** | [`detect_spot_termination.sh`](runtime_spot/monitoring/detect_spot_termination.sh) | Monitors for AWS Spot shutdown notice in the background |
| **10. Save Checkpoint** | [`checkpoint_save.py`](ml/checkpoint_save.py) | Saves training progress to S3 at specified intervals (epochs) |
| **11. Terminate EC2 Instance** | [`09_terminate_ec2.sh`](runtime_spot/09_terminate_ec2.sh) | Ensures cleanup and Spot Instance termination | 
