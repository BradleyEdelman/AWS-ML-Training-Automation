# AWS CLI Installation Guide

This guide covers **installing AWS CLI** for Windows. As I am using a windows machine, this and other docs are geared towards Windows users as well. Mac OS and Linux commands are very similar, but require slight modifications.

---

## **Step 1: Install AWS CLI**
AWS CLI is required for interacting with AWS services.

### **Windows**
1. Download & install [AWS CLI for Windows](https://awscli.amazonaws.com/AWSCLIV2.msi).

- You can also install it by running the following in **Git Bash**
```bash
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

2. Verify installation:

```bash
aws --version
```

---

## **Step 2: Install Git Bash and Dependencies**
Git Bash provides Unix-like shell for Windows, and you must install it in order to run shell scripts on Windows.

Git Bash should come pre-installed on your Windows, but if not:
1. Go to the official Git for [Windows download page](https://git-scm.com/downloads).
2. Download and install Git Bash.
3. During installation, select Use Git and Optional Unix Tools from Command Prompt.

Open Git Bash and navigate to the repository folder:

```bash
cd /path/to/repo/
```

Run the "install_shell_dependencies.sh" shell script in Git Bash to install necessary dependencies:

```bash
bash setup/install_shell_dependecies.sh
```
