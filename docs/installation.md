# Installation Guide

This guide will help you set up **The Jolly Method** stack from scratch.

## Prerequisites

- **OS:** Linux (Ubuntu/Debian recommended) or macOS.
- **Python:** 3.11 or higher.
- **Docker:** Required for Open WebUI.
- **Node.js:** Required for `gemini-cli`.

## 1. Install CLI Tools (The Models)

The Jolly Method uses a "Subscription-First" approach. We use the CLI tools provided by AI vendors to leverage fixed-monthly-cost subscriptions instead of per-token APIs.

### A. Claude (Anthropic)
Requires a Claude Pro subscription ($20/mo).

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

### B. Gemini (Google)
Requires a Google One AI Premium subscription ($20/mo).

```bash
npm install -g @google-ai/gemini-cli
gemini-cli auth login
```

### C. Ollama (Local)
Free and unlimited local models.

1.  Install from [ollama.com](https://ollama.com).
2.  Pull a coding model:
    ```bash
    ollama pull qwen2.5-coder:14b
    ```

## 2. Install CLIProxyAPI (The Gateway)

This tool wraps the CLIs above into a standard OpenAI-compatible API that our agents can talk to.

```bash
git clone https://github.com/router-for-me/CLIProxyAPI.git
cd CLIProxyAPI
pip install -r requirements.txt

# Start the server (consider running as a systemd service)
python main.py
```

*Note: Ensure it is running on port 8317 (or configure port in main.py).*

## 3. Install jolly-flow (The Agents)

This is the core orchestration engine.

```bash
# Clone this repository
git clone https://github.com/thejollydev/the-jolly-method.git
cd the-jolly-method/jolly_flow

# Install using uv (recommended)
pip install uv
uv pip install -e .

# Or standard pip
pip install -e .
```

## 4. Install Open WebUI (The Interface)

We use Open WebUI for a nice chat interface. We must run it with specific flags to enable our custom integrations.

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e ENABLE_TOOLS=true \
  -e ENABLE_FUNCTIONS=true \
  -v open-webui:/app/backend/data \
  -v /home/joseph/GoogleDrive:/home/joseph/GoogleDrive \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

*Important: The `-v /home/...` mount allows the container to see your project files. Adjust the path to match your actual Google Drive or project location.*

## 5. Post-Install Configuration

1.  Go to `http://localhost:3000`.
2.  Create an admin account.
3.  Go to **Admin Panel > Functions**.
4.  Click **+** (Import/Create).
5.  Copy the code from `src/jolly_flow/pipelines/jolly_pipeline.py` in this repo.
6.  Paste it into the editor, save, and toggle **On**.

You are now ready to use The Jolly Method!
