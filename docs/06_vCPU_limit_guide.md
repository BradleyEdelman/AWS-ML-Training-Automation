# vCPU Limit Guide

This guide explains how to **check, request, and monitor vCPU limit increases** in AWS. Increasing the vCPU limit is required to **launch GPU instances** for machine learning and training.
  
- First-time requests may require **manual AWS approval** (email notifications will be sent).  
- This guide covers **AWS CLI commands only**, which should be sufficient for most users.

---

Attach the following to your **EC2-Training-Role** permission policy to allow vCPU limit management:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ServiceQuotasVCpuLimits",
            "Effect": "Allow",
            "Action": [
                "servicequotas:GetServiceQuota",
                "servicequotas:GetAWSDefaultServiceQuota",
                "servicequotas:ListAWSDefaultServiceQuotas",
                "servicequotas:ListRequestedServiceQuotaChangeHistory",
                "servicequotas:RequestServiceQuotaIncrease"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## **Step 1: Identify Your Current vCPU Limits**
To check your current vCPU limits for a specific AWS region:

```bash
aws service-quotas get-service-quota \
    --service-code ec2 \
    --quota-code L-34B43A08 \
    --region region
```

## **Step 2: Request a Limit Increase**
To request an increase for the On-Demand vCPU Limit, run:

```bash
aws service-quotas request-service-quota-increase \
    --service-code ec2 \
    --quota-code L-34B43A08 \
    --desired-value 24 \
    --region region
```

## **Step 3: Check the Status of Your Request**

To check the status of your request:
```bash
aws service-quotas list-requested-service-quota-change-history \
    --service-code ec2 \
    --region region
```

This will return a list of requests and their statuses (PENDING, APPROVED, DENIED).

---

Other EC2 Service Quotas codes:
- L-1216C47A: On-Demand Standard Instance vCPUs
- L-34B43A08: Spot Instance vCPUs
- L-7212CCBC: Dedicated Host vCPUs
- L-7E9ECCDB: Running Dedicated vCPUs
- L-F98A55E5: Running On-Demand G/VT/P Instance vCPUs (GPU instances)