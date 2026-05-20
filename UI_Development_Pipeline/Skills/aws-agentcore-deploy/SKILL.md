---
name: aws-agentcore-deploy
description: Guides the creation, local development, and serverless deployment of AI Agents using the Amazon Bedrock AgentCore CLI.
license: MIT
skill-author: AROS-System
---

# Amazon Bedrock AgentCore Deploy

## Overview
This skill provides the standard workflow for scaffolding, testing, and deploying AI agent applications on AWS using the `agentcore` CLI. It supports agents built with frameworks like LangGraph, CrewAI, or standard Python/TypeScript.

## Workflow Execution

### 1. Initialization
When a user requests a new AI agent deployment on AWS:
1.  Ensure Node.js and the CLI are installed (`npm install -g @aws/agentcore`).
2.  Use the wizard to create the project structure:
    ```bash
    agentcore create
    ```

### 2. Capabilities Configuration
AgentCore provides several managed capabilities. Use the CLI to add them to the project before deployment:
*   Memory: `agentcore add memory`
*   Identity: `agentcore add identity`
*   Evaluation: `agentcore add evaluator`

### 3. Local Development
*   Always test the agent locally before deploying to AWS to save costs and verify logic.
    ```bash
    agentcore dev
    ```

### 4. Deployment
*   Deploy the agent securely at scale to the serverless Amazon Bedrock AgentCore Runtime.
    ```bash
    agentcore deploy
    ```
*   Test the deployed endpoint:
    ```bash
    agentcore invoke
    ```

## Important Considerations
- Bedrock AgentCore supports both Python (using `uv` for dependency management) and TypeScript. 
- Ensure that the local AWS credentials used have the `BedrockAgentCoreFullAccess` and `AmazonBedrockFullAccess` policies attached.
