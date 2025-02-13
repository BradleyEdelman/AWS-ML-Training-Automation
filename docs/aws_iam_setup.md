# AWS IAM Role Setup Guide

This guide provides step-by-step instructions to obtain the IAM access required to run the automated ML scripts. Since most users do not have root access, they must request IAM permissions from their AWS administrator. These items can be found in **Option 1** below. Individuals with root access can also create a new IAM role/user themselves, as described in **Option 2**.

---

## Option 1: No AWS Root Access 

### Request an **IAM role**: e.g. `EC2-Training-Role`

### **Required AWS Managed Policies:**
- S3 (`your-bucket-name`)
    - **s3:GetObject**
    - **s3:PutObject**
    - **s3:ListBucket**
- EC2
    - **ec2:DescribeInstances**
    - **ec2:StartInstances**
    - **ec2:StopInstances**
    - **ec2:TerminateInstances**
    - **ec2:RequestSpotInstances**
    - **ec2:CancelSpotInstanceRequest**
- CloudWatchLogs
    - **CreateLogStream**
    - **PutLogEvents**

Once the AWS admin creates the IAM role, they will provide you with an IAM Role ARN (Amazon Resource Name), which you must insert into the **config.yaml** file

Example IAM ARN: `arn:aws:iam::YOUR_ACCOUNT_ID:role/EC2-Training-Role`

### **Access & Secret Key**
Users must also request:  
- **AWS Access Key ID**
- **AWS Secret Access Key**

### **S3 Bucket name** 
Users will also need a dedicated S3 bucket:
Example S3 Bucket: `s3://your-bucket-name/`

---

## Option 2: AWS Root Access (via AWS dashboard)

## **Step 1: Create an S3 bucket**
1. Open the **AWS Console** and navigate to **S3**.
2. Click on "Create bucket"
3. Name the bucket **`EC2-Training-Bucket`**, and then click "Create bucket" at the bottom of the page.
   
## **Step 2: Create an IAM role**
1. Navigate to the **IAM Dashboard**.
2. Click on **Roles** in the lefthand menu.
3. Click **Create Role**.
4. For **Select Trusted Entity Type** choose **AWS Service**.
5. FOr **Use Case** select **EC2** from the dropdown menu and click "next".

6. Do not add any permissions, and click "next".

7. Name the role `EC2-Training-Role`, do not modify the trust policy and click "create role"

### **Step 3: Attach a Custom Permission Policy to IAM role**
1. Navigate back to **Roles** in the **IAM Dashboard**.
2. Click on  **`EC2-Training-Role`**
3. Under the **Permissions** tab, click on **Add permissions** and select **Create inline polic**
4. In the Policy editor click on **"JSON"** an replace the existing text with the restricted IAM policy below (be sure to replace "your-bucket-name", "region", and "account-id" with your own). Click "next".
5. Enter **"EC2-Training-Policy"** for the Policy name and click "Create policy"

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
```

## **Step 4: Create an IAM User**
1. Navigate to the **IAM Dashboard**.
2. Click on **Users** in the lefthand menu.
3. Click **Create User**.
4. Enter **`EC2-Training-User`** in User name, and click "next".
5. If desired, add this User to a User group. Otherwise, click "next".
6. Click "Create user".
7. Click on `EC2-Training-User` and copy the ARN in the Summary box

Example IAM ARN: `arn:aws:iam::YOUR_ACCOUNT_ID:role/EC2-Training-Role`

## **Step 5: Modify the IAM Role Trust Policy**
Allow a specific IAM User to assume this role.

1. Navigate back to **Roles** in the **IAM Dashboard** and click on the **`EC2-Training-Role`**.
2. Click on the **"Trust relationships"** tab and then **"Edit trust policy"**
3. Replace the existing text with the trust policy below (be sure to replace "YOUR_ACCOUNT_ID" with you own). Click "Update policy"
   
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
```

## **Step 6: Create access key for IAM User**
1. Navigate back to **Users** in the **IAM Dashboard** and click on the **`EC2-Training-User`**.
2. On the right side of the Summary box, click **"Create access key"**.
3. For User case select **"Command Line Interface (CLI)"**, check the confirmation box at the bottom of the page, and click "next".
4. Enter **`EC2-Training-Key`** in the Description tag value box and click "Create access key"
5. Click the "Download .csv file" at the bottom of the page to save the access and secret key, and then click "done"
