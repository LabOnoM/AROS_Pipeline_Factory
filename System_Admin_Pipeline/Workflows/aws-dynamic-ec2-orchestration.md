# `/aws-dynamic-ec2-orchestration`

Trigger this workflow when working on the `AWS_DynamicEC2` project or when implementing autonomous logic to scale AWS instances based on active application connections.

## Objective
To orchestrate dynamic, cost-saving EC2 start/stop operations. The system monitors Shiny Server processes using a Python daemon (`pyCount.py`) and toggles EC2 infrastructure via Boto3 depending on demand.

## Prerequisites
- **AWS Credentials:** Ensure the local environment has configured AWS CLI credentials with sufficient IAM permissions to invoke `ec2:DescribeInstances`, `ec2:StartInstances`, and `ec2:StopInstances`.
- **Skills:** Agents MUST employ the `aws-boto3-manager` skill to write idempotent AWS infrastructure code.

## Step-by-Step Implementation

### Step 1: Process Monitoring Audit
1. Audit the `pyCount.py` daemon responsible for monitoring Shiny-server processes.
2. Verify that the script safely counts active WebSocket or HTTP connections to the server.

### Step 2: Boto3 Integration
1. Implement the `boto3` logic to check the status of the target EC2 instances.
2. Embed the start/stop triggers. Ensure that the logic is idempotent (e.g., do not send a "stop" command if the instance is already "stopping" or "stopped").
3. Implement `Waiters` if the script needs to block execution until the instance is fully `running`.

### Step 3: Application Embedding
1. Integrate the `boto3` status check into the R/Shiny application logic (via the templates in `app-code` or `ui-server-code`).
2. The user interface must seamlessly inform the end-user if the backend EC2 server is currently waking up, preventing timeout errors.

### Step 4: Verification
1. Run local execution tests using `boto3` dry-run features where possible.
2. Validate systemd service (`pyCount.service`) deployment paths and log output for the daemon.
