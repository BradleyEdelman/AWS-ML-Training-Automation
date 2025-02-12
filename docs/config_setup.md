# Config File (`config.yaml`) Setup Guide 

This guide explains the **configuration settings** in `config.yaml`, which controls the AWS ML training automation process.  

**Why use `config.yaml`?**  
- Keeps **user settings separate** from automation scripts.  
- Allows easy customization of **AWS resources, model training, and storage settings**.  
- Ensures that users **do not have to modify scripts manually**.  

---

## **1️. AWS Configuration**

These settings define **IAM role permissions, AWS region, and storage bucket**.

```yaml
aws:
  iam_role_arn: "arn:aws:iam::123456789012:role/EC2-Training-Role"
  region: "us-east-1"
  s3_bucket: "your-bucket-name"
