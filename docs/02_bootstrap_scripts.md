# Bootstrap Scripts Guide

This document explains the purpose and functionality of the bootstrap scripts that are used to set up the IAM role required to use this package.

---

## Overview

The bootstrap scripts automate the AWS IAM role setup, ensuring necessary permissions are in place for launching Spot Instances and interacting with AWS services.

| Script | Description |
|--------|-------------|
| `00_install_shell_requirements_client.sh` | Automatically installs the shell requirements in "requirements-sh.txt that are needed to run shell scripts in this package. |
| `01_iam_role_setup.sh` | Creates an IAM role with the required permissions for EC2, S3, and CloudWatch. This script also attaches the necessary policies. |

---

## **01_iam_role_setup.sh** - IAM Role Setup  
This script sets up an IAM role with predefined permissions:
1. Creates the IAM role if it doesn’t exist.
2. Attaches a trust policy allowing the specified user to assume the role.
3. Assigns permissions for EC2 management, S3 access, and CloudWatch logging (amongst other minor capabilities).
4. Prints the IAM role ARN for reference.

### **Usage**
Run the script from the client machine:
```bash
bash bootstrap/01_iam_role_setup.sh
```
