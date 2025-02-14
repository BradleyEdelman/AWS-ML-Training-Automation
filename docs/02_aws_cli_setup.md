# AWS CLI Setup Guide

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

3. Verify access to S3, EC2, and Cloudwatch 

- Check S3 Access
```bash
aws s3 ls s3://your-bucket-name
```

This should return the contents of your bucket, or nothing if it is empty

- Check EC2 Access
```bash
aws ec2 describe-instances
```

This should return the following if no instances have been connected to your account:
```json
{
    "Reservations": []
}
```

- Check CloudWatch 
```bash
aws logs describe-log-groups
```

This should return a list of all log groups, similar to that below:
```json
{
    "logGroups": [
        {
            "logGroupName": "/aws/ec2/training-logs",
            "creationTime": 1739460770769,
            "metricFilterCount": 0,
            "arn": "arn:aws:logs:region:account-id:log-group:/aws/ec2/training-logs:*",
            "storedBytes": 0,
            "logGroupClass": "STANDARD",
            "logGroupArn": "arn:aws:logs:region:account-id:log-group:/aws/ec2/training-logs"
        }

```

If you see these outputs, your temporary credentials are working and you can proceed to uploading data to your s3 bucket and requesting resources for ML training.


<!-- 
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

--- -->



