---
name: aws-boto3-manager
description: Safely manages AWS operations via the Python boto3 SDK, utilizing standard local AWS CLI credentials to interact with EC2, S3, and API Gateway.
license: MIT
skill-author: AROS-System
---

# AWS Boto3 Manager

## Overview
This skill governs how AROS agents interact programmatically with AWS using the `boto3` library in Python. It provides the standard operating procedures for executing dynamic infrastructure operations, such as orchestrating EC2 instances, reading from S3, or publishing to SNS topics.

## Execution Rules

### 1. Authentication
Agents MUST NOT hardcode AWS credentials (Access Key ID or Secret Access Key) into any script.
*   **Rule:** Always use standard local AWS CLI credentials. Rely on the default credential provider chain (`~/.aws/credentials`, environment variables, or IAM instance profiles).
*   **Initialization:** 
    ```python
    import boto3
    # Use default session
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ```

### 2. EC2 State Orchestration
When writing scripts to dynamically start or stop EC2 instances based on demand (e.g., for Shiny Server scaling):
*   Use `ec2.describe_instances()` to check the current state (`pending`, `running`, `stopping`, `stopped`).
*   Always implement explicit Waiters if synchronous execution is required after a state change command:
    ```python
    # Start instance
    ec2.start_instances(InstanceIds=['i-0abcd1234efgh5678'])
    # Wait for running state
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=['i-0abcd1234efgh5678'])
    ```

### 3. Error Handling
*   **Rule:** Wrap API calls in `try...except` blocks using `botocore.exceptions.ClientError` to gracefully handle permissions errors, rate limits (Throttling), or invalid resource IDs.

### 4. Idempotency
Ensure that infrastructure modification scripts are idempotent. For example, before sending a `start_instances` command, verify the instance is not already in the `running` state to avoid unnecessary API calls.
