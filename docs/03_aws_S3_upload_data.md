# Upload Data to S3 Guide

Once you or your administrator has created your **Amazon S3** bucket and given you access, you can upload data. Using the AWS CLI is preferred for files over 5GB. Furthermore, for these large files, it is not possible to move them once uploaded so make sure that the final destination is specified during upload.

---

## **Upload via AWS CLI**

### **Step 1: Assume IAM role**
- Run the following to assume your IAM role

```bash
. scripts/assume_iam_role.sh
```

- Verify S3 bucket access

```bash
aws s3 ls s3://your-bucket-name
```

If your bucket is empty, nothing will be returned. Otherwise, you should see a list of files/folders currently in your bucket. If an error is shown, check your permissions and whether you correctly assumed the IAM role.

### **Step 2: Upload data**
- Upload a single file

```bash
aws s3 cp //path//to/local-file s3://your-bucket-name/path/in-bucket/
```

- Upload an entire directory

```bash
aws s3 cp //path//to//local-folder s3://your-bucket-name/path/in-bucket/ --recursive
```

- Verify S3 Upload Was Successful

```bash
aws s3 ls s3://your-bucket-name/path/in-bucket/
```