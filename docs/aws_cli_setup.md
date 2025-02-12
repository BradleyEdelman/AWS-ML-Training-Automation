# AWS CLI  Setup Guide

This guide provides step-by-step instructions set up the AWS command line interface (CLI) for uploading data, requesting EC2 spot instances, and running jobs.

---

## 1. Install AWS Command Line Interface (CLI)  

AWS CLI is required to test IAM role functionality and interact with AWS services.  

### **Install AWS CLI**  

#### **For macOS & Linux**  
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
# Verify installation
aws --version
```

#### **For Windows**  
1. Download the [AWS CLI Windows Installer](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2. Run the installer and follow the on-screen instructions.
3. Verify installation in Command Prompt:

```bash
# Verify installation
aws --version
```

---

## 2. Configure AWS CLI

Once installed, configure AWS CLI using your Access Key & Secret Key:

```bash
aws --configure
```

It will prompt for:

- AWS Access Key ID → Enter the key provided by your AWS admin.
- AWS Secret Access Key → Enter the secret key.
- Default AWS Region → Use your **assigned AWS region** (e.g., `us-east-1`).
- Output format → Enter `json` (recommended).

```bash
# Verify configuration
aws configure list
```

---

## 3. Verify IAM Role is Active

After receiving the IAM Role, verify that it exists and has the correct policies attached:

```bash
aws iam get-role --role-name EC2-Training-Role
```

This should return details about the role, including its ARN and attached policies.

---

## 4. Manually Attach IAM Role to EC2 Instances

Since you do not have root access, you must manually attach the IAM role when launching an EC2 instance via AWS Console or CLI.

- Attach IAM Role via AWS CLI

When launching an EC2 instance from the CLI, specify the IAM Role like this:

```bash
aws ec2 run-instances \
    --image-id ami-xxxxxxxxxxxxx \
    --count 1 \
    --instance-type g4dn.xlarge \
    --iam-instance-profile Name=EC2-Training-Role
```

---

## 5. Upload Data to S3 Using AWS CLI

Once you receive the S3 bucket name, upload your training data to it using AWS CLI. Using the CLI is required for files/folders larger than 5GB.

- Upload a single file

```bash
aws s3 cp /path/to/local-file s3://your-bucket-name/path/in-bucket/
```

- Upload an entire directory

```bash
aws s3 cp /path/to/local-folder s3://your-bucket-name/path/in-bucket/ --recursive
```

- Verify S3 Upload Was Successful

```bash
aws s3 ls s3://your-bucket-name/path/in-bucket/
```

---

## 6. Test IAM Role Functionality

Once your EC2 instance is running with the attached IAM role, confirm that it can access AWS services:

- Check S3 Access

```bash
aws s3 ls s3://your-bucket-name
```

If this command returns a list of files, your permissions are correctly set up.

- Check EC2 Access

```bash
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]'
```

This should return details of running EC2 instances.

---

📌 Next Steps

Modify config.yaml to include the correct IAM Role ARN.

Proceed with running deploy_training.sh to launch an EC2 training instance.


