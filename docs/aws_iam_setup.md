# AWS IAM Role Setup Guide

This guide provides step-by-step instructions to request and configure IAM permissions that are needed for AWS EC2 ML training automation. Since most users do not have root access, they must request IAM permissions from their AWS administrator.

---

## 1️. Request Required IAM Permissions

To enable the scripts to interact with AWS services (EC2, S3, and logging), users should request the following IAM permissions from their administrator:

### **IAM Role Name:** `EC2-Training-Role`

### **Required AWS Managed Policies:**
- **`AmazonS3FullAccess`** → Required for saving/loading training checkpoints.
- **`CloudWatchLogsFullAccess`** → Required for logging training progress.
- **`AmazonEC2FullAccess`** → Required for managing EC2 instances.

### **Request Access & Secret Key**
Users must also request:  
- **AWS Access Key ID**
- **AWS Secret Access Key**

💡 **These credentials are required to configure AWS CLI.**
⚠️ **Store them securely and do not share them publicly.**

### **Obtain IAM Role ARN**

Once the AWS admin creates the IAM role, they will provide you with an IAM Role ARN (Amazon Resource Name), which you must insert into the **config.yaml** file (LATER.MD)

Example IAM ARN: `arn:aws:iam::123456789012:role/EC2-Training-Role`

### **Request S3 Bucket name** 

Example S3 Bucket: `s3://your-bucket-name/`

---


This guide walks through **creating an IAM Role**, **attaching it to an IAM User**, and **configuring AWS CLI** for ML training automation.

---

## **1️⃣ Create an IAM Role for EC2 Training**
To allow AWS services (EC2) and users to interact with AWS resources (S3, CloudWatch, etc.), we need an **IAM Role**.

### **Step 1: Go to IAM Roles**
1. Open the **AWS Console** → Navigate to **IAM → Roles**.
2. Click **Create Role**.
3. **Select Trusted Entity Type** → Choose **AWS Service**.
4. **Choose a Use Case** → Select **EC2** → Click **Next**.

### **Step 2: Attach a Custom Policy**
1. Click **"Create Policy"** and switch to the **JSON tab**.
2. Copy and paste the following **restricted IAM policy**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3LimitedAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        },
        {
            "Sid": "EC2RestrictedActions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances",
                "ec2:RequestSpotInstances",
                "ec2:CancelSpotInstanceRequests"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchLoggingLimited",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:region:account-id:log-group:/aws/ec2/training-logs"
        }
    ]
}


3. Click Next, name the policy (EC2TrainingPolicy), and click Create Policy.
4. Go back to IAM Role Creation → Attach EC2TrainingPolicy.
5. Click Next → Name the Role (EC2-Training-Role) → Create Role.


2️⃣ Modify the IAM Role Trust Policy
Now, allow a specific IAM User to assume this role.

Step 1: Edit the Trust Policy
Go to IAM → Roles → Click EC2-Training-Role.

Click "Trust relationships" → "Edit trust policy".

Replace with:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/EC2-Training-User"
            },
            "Action": "sts:AssumeRole"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
4. Click "Update Policy".