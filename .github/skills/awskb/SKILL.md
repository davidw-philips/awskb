---
name: awskb
description: Access AWS documentation, SDKs, service availability, regions, and AWS agent skills dynamically via the AWS Knowledge MCP service. Use when you need precise information on AWS services, API references, CDK/CloudFormation constructs, troubleshooting, or regional availability.
---

# AWS Knowledge Base CLI (`awskb`)

`awskb` is a lightweight, token-efficient command-line interface to the official remote AWS Knowledge MCP service (`https://knowledge-mcp.global.api.aws`).

Rather than dumping full MCP tool schemas into agent context up front, query `awskb` dynamically to discover tools and retrieve only the documentation or skills needed.

## Pre-requisite / Installation Check

Before running `awskb` commands, check if the CLI is available in the environment:

```bash
which awskb || command -v awskb || Get-Command awskb
```

**If `awskb` is not installed**, refer to [INSTALL.md](INSTALL.md) or install it immediately:
- **Fastest via `uv`:** `uv tool install git+https://github.com/davidw-philips/awskb`
- **On-the-fly execution via `uvx`:** prefix commands with `uvx --from git+https://github.com/davidw-philips/awskb awskb ...`
- **Via `pipx` or `pip`:** `pipx install git+https://github.com/davidw-philips/awskb.git` or `pip install git+https://github.com/davidw-philips/awskb.git`

## When to Use

Use `awskb` whenever you need:
- Information on how AWS services, APIs, and SDKs work
- Code examples and API parameter specifications for AWS SDKs (boto3, JS v3, Go SDK, etc.)
- AWS CDK constructs, patterns, and CloudFormation template references
- AWS region codes and identifiers
- Regional availability for AWS services, APIs, and CloudFormation resources
- Domain-specific AWS agent skills, workflows, and procedures
- Troubleshooting guides and solutions for AWS errors

## Workflow & Commands

### 1. Discover Available Capabilities
Fetch available tools directly from the remote MCP endpoint:
```bash
awskb --help
```

### 2. Inspect Tool Instructions On-Demand (Token Saver)
Retrieve the exact description, schema, and parameter guidance for a specific tool:
```bash
awskb --tool <tool_name> description
```
*Aliases supported*: `aws___<tool_name>` or short names like `search_documentation`, `read_documentation`, `list_regions`, `get_regional_availability`, `retrieve_skill`.

### 3. Execute MCP Tools
Call any tool with JSON arguments:

- **Search AWS Documentation**:
  ```bash
  awskb call search_documentation '{"search_phrase": "DynamoDB global tables multi-region write"}'
  ```

- **Read Specific AWS Documentation Page**:
  ```bash
  awskb call read_documentation '{"requests": [{"url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html"}]}'
  ```

- **List All AWS Regions**:
  ```bash
  awskb call list_regions
  ```

- **Check Regional Availability**:
  ```bash
  awskb call get_regional_availability '{"regions": ["us-east-1", "eu-west-1"], "resource_type": "product", "filters": ["Amazon Bedrock"]}'
  ```

- **Retrieve Domain-Specific AWS Agent Skill**:
  ```bash
  awskb call retrieve_skill '{"skill_name": "<skill_name>"}'
  ```

## Rules & Best Practices
- **Do not guess documentation URLs**: Always run `awskb call search_documentation ...` first. Its results contain verbatim text chunks that often answer the question directly.
- **Inspect before calling unfamiliar tools**: Run `awskb --tool <tool_name> description` to verify required parameters before calling.
- **Cross-platform**: `awskb` runs with Python 3 / `uvx` / `pip` across Linux, macOS, and Windows.
