# Upload Data to S3

This guide provides step-by-step instructions for uploading  datasets to **Amazon S3**

---

## **Option 1: Upload via AWS Console**
1. Open the **AWS Console** and navigate to **S3**.
2. **Select your bucket**: `your-bucket-name`
3. Click **"Upload"**.
4. Drag & drop files or click **"Add files"** to select them from your system.
5. Click **"Upload"**.

---

## **Option 2: Upload via AWS CLI**
Use the AWS CLI if you have large datasets or want to automate uploads. Using the CLI is required for files/folders larger than 5GB.

### **Upload a Single File**
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