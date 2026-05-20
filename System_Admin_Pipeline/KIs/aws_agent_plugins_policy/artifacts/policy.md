# AWS Agent Plugins Policy

This Knowledge Item standardizes how AROS interacts with and constructs **Agent Plugins for AWS**. These plugins equip AI coding agents with the skills to architect, deploy, and operate on AWS infrastructure seamlessly. 

## Architectural Concept
Agent plugins act as containers that package different types of expertise artifacts together to steer coding agents toward reliable outcomes without bloating the model context. 

A single agent plugin in the AROS/AWS ecosystem must consist of:
1. **Agent Skills (Workflows):** Structured step-by-step processes. For example, guiding an AI through deploying to AWS, reviewing code for serverless architecture, or setting up auth.
2. **MCP Servers (Connections):** External data sources such as real-time pricing (`awspricing`), AWS Knowledge docs (`awsknowledge`), or deployment IaC guidance (`aws-iac-mcp`).
3. **Hooks (Guardrails):** Automation that runs on developer actions. E.g., validating a `template.yaml` whenever it is modified.
4. **References (Knowledge):** Documentation, configuration defaults, and context.

## Best Practices for AROS Agents
When an AROS Swarm agent leverages AWS plugins (such as `deploy-on-aws` or `aws-serverless`), they must follow these essential guidelines:
- **Least Privilege:** Always configure local AWS credentials or IAM Roles using the principle of least privilege.
- **Review over Auto-deploy:** Always present the generated Infrastructure as Code (CDK, CloudFormation) to the user for review before executing deployment commands.
- **Cost Estimation:** Before provisioning any AWS resources, use the `awspricing` MCP to estimate costs and request user confirmation.

## Amazon Bedrock AgentCore
When building native AI Agents on AWS, AROS agents should utilize **Amazon Bedrock AgentCore**. It is a framework-agnostic runtime that allows agents built in LangGraph, CrewAI, etc., to be deployed serverlessly on AWS.
- **CLI Workflow:** `agentcore create` -> `agentcore dev` -> `agentcore deploy`
- Capabilities include: Identity management, Memory, Code Interpreter, and Observability.
