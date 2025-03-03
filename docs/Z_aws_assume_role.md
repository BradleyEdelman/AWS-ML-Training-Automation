# AWS Assume Role Guide

This guide covers how to **assume an IAM role** using AWS CLI and verify access. Users must assume their IAM role in order to access the AWS services described in the IAM setup instructions.

---

## **Step 1: Assume Role via AWS CLI**
Run:
```bash
. scripts/assume_iam_role.sh
```

This script will:
- Assume IAM role
- Fetch temporary credentials
- Export credentials for your terminal session


## **Step 2: Verify Role Access**

Check role identity:

```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "ARO123456789:EC2TrainingSession",
    "Account": "account-id",
    "Arn": "arn:aws:sts::account-id:assumed-role/EC2-Training-Role/EC2TrainingSession"
}
```

If it returns EC2TrainingSession, you have successfully assumed the role. If not, clean the keys and try again:

```bash
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_PROFILE
. scripts/assume_iam_role.sh
aws sts get-caller-identity
```

## **Step 3: Validate AWS permissions**


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
