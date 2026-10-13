# Installing `awskb`

The `awskb` CLI provides agents and developers with dynamic, token-efficient access to the remote AWS Knowledge MCP Server (`https://knowledge-mcp.global.api.aws`).

It has **zero third-party dependencies** (uses only standard library Python 3) and runs seamlessly on Windows, macOS, and Linux.

---

## 1. Quick Verification

Before installing, check if `awskb` is already present in your PATH:

```bash
which awskb || command -v awskb || Get-Command awskb
```

Or test invocation directly:
```bash
awskb --help
```

---

## 2. Installation Options

### Option A: Install via `uv` (Recommended)
If `uv` is installed, install `awskb` as a globally isolated tool:
```bash
uv tool install git+https://github.com/davidw-philips/awskb
```

To update later:
```bash
uv tool upgrade awskb
```

---

### Option B: Run on the fly with `uvx` (No installation needed)
If you don't want to install anything permanently, run `awskb` on demand via `uvx`:
```bash
uvx --from git+https://github.com/davidw-philips/awskb awskb --help
```

---

### Option C: Install via `pipx`
If using `pipx`:
```bash
pipx install git+https://github.com/davidw-philips/awskb.git
```

---

### Option D: Install via `pip`
```bash
pip install git+https://github.com/davidw-philips/awskb.git
```

---

### Option E: Local Development / Clone
Clone the repository and install in editable mode:
```bash
git clone https://github.com/davidw-philips/awskb.git
cd awskb
pip install -e .
```
