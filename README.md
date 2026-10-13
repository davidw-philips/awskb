# awskb

`awskb` is a lightweight, cross-platform CLI tool for interacting with the official [AWS Knowledge MCP Server](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server) (`https://knowledge-mcp.global.api.aws`).

Designed for humans and AI agents (GitHub Copilot, Claude Code, OpenAI Codex, Cursor) to dynamically fetch AWS documentation, SDK parameters, regional availability, and AWS agent skills without polluting model context windows with giant MCP tool schemas.

## Installation & Running

Works identically on **Windows**, **macOS**, and **Ubuntu/Linux** with zero third-party dependencies (pure standard library).

### Option 1: Run directly without installation (using `uvx`)
```bash
uvx --from git+https://github.com/davidw-philips/awskb awskb --help
```

### Option 2: Install globally with `uv`
```bash
uv tool install git+https://github.com/davidw-philips/awskb
```

### Option 3: Install with `pip` / `pipx`
```bash
pipx install git+https://github.com/davidw-philips/awskb.git
# or
pip install git+https://github.com/davidw-philips/awskb.git
```

### Option 4: Local Editable Install
```bash
pip install -e .
```

---

## Usage

### 1. Dynamic Tool Discovery
List all tools available on the remote MCP endpoint:
```bash
awskb --help
```

### 2. Inspect Tool Description & Input Schema
To save tokens, query detailed guidance only for the tool you plan to call:
```bash
awskb --tool search_documentation description
```

### 3. Execute MCP Tools
Call any tool using JSON arguments:

- **Search AWS Documentation**:
  ```bash
  awskb call search_documentation '{"search_phrase": "Amazon Bedrock Converse API"}'
  ```

- **Read Specific AWS Documentation Page**:
  ```bash
  awskb call read_documentation '{"requests": [{"url": "https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html"}]}'
  ```

- **List All AWS Regions**:
  ```bash
  awskb call list_regions
  ```

- **Check Regional Availability**:
  ```bash
  awskb call get_regional_availability '{"regions": ["us-east-1"], "resource_type": "product", "filters": ["Amazon Bedrock"]}'
  ```

- **Retrieve AWS Agent Skill**:
  ```bash
  awskb call retrieve_skill '{"skill_name": "example_skill"}'
  ```

---

## Agent Skills Included

Pre-packaged skills following official agent specifications are provided for:
- **GitHub Copilot**: [.github/skills/awskb/SKILL.md](.github/skills/awskb/SKILL.md)
- **Claude Code**: [.claude/skills/awskb/SKILL.md](.claude/skills/awskb/SKILL.md) (with `allowed-tools: Bash(*)`)
- **OpenAI Codex**: [.agents/skills/awskb/SKILL.md](.agents/skills/awskb/SKILL.md) and [.codex/skills/awskb/SKILL.md](.codex/skills/awskb/SKILL.md) (supports standard repo root discovery)
