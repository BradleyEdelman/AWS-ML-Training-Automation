# AWS CLI  Setup Guide

This guide provides step-by-step instructions set up the AWS command line interface (CLI) for uploading data, requesting EC2 spot instances, and running jobs.

---

## **Step 1. Install AWS Command Line Interface (CLI)**

AWS CLI is required to test IAM role functionality and interact with AWS services.  

### **Install AWS CLI**  
1. Follow the instructions for the [AWS CLI Windows Installer](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) depending on your OS.

2. Verify installation
   
```bash
aws --version
```

---

## **Step 2. Configure AWS CLI**

Once installed, configure AWS CLI using your **IAM User Access Key & Secret Key**:

```bash
aws configure --profile ec2-training
```

It will prompt for:

- AWS Access Key ID - Enter the key provided by your AWS admin.
- AWS Secret Access Key - Enter the secret key.
- Default AWS Region - Use your **assigned AWS region** (e.g., `eu-central-1`).
- Output format - Enter `json` (recommended).

After running the following command, you should  see the `ec2-training` profile listed:
```bash
aws configure list-profiles
```

Similarly, running the below code should print out the details that you previously entered:
```bash
aws configure list --profile ec2-training
```

---

## **Step 3. Assume the IAM role**

1. Since the IAM user does not have direct permissions, it must assume the role.

###
```bash
aws sts assume-role --role-arn "arn:aws:iam::YOUR_ACCOUNT_ID:role/EC2-Training-Role" --role-session-name "EC2TrainingSession" --profile ec2-training
```

If successful, it should print an output similar to that below:

```json
{
    "Credentials": {
        "AccessKeyId": "TEMP_ACCESS_KEY",
        "SecretAccessKey": "TEMP_SECRET_KEY",
        "SessionToken": "TEMP_SESSION_TOKEN"
    },
    "AssumedRoleUser": {
        "Arn": "arn:aws:sts::YOUR_ACCOUNT_ID:assumed-role/EC2-Training-Role/EC2TrainingSession"
    }
}
```

2. Set temporary credentials

Since the credentials are temporary, set them before running AWS CLI commands:

```bash
set AWS_ACCESS_KEY_ID=TEMP_ACCESS_KEY
set AWS_SECRET_ACCESS_KEY=TEMP_SECRET_KEY
set AWS_SESSION_TOKEN=TEMP_SESSION_TOKEN
```





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


