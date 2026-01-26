# Installation Guide

This guide covers the complete setup of the **jolly-flow** ecosystem.

## 📋 Prerequisites

- **OS:** Linux (preferred) or macOS.
- **Python:** 3.11+
- **Docker:** (Optional) For the Web Interface.
- **Node.js:** For CLI tool authentication.

---

## 1. AI Providers (Subscriptions)

`jolly-flow` leverages your existing subscriptions to avoid per-token API costs.

### Claude (Anthropic)
Requires **Claude Pro**.
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

### Gemini (Google)
Requires **Google One AI Premium**.
```bash
npm install -g @google-ai/gemini-cli
gemini-cli auth login
```

### Ollama (Local)
Free, unlimited local models.
1. Download from [ollama.com](https://ollama.com).
2. Pull the recommended model: `ollama pull qwen2.5-coder:14b`.

---

## 2. CLIProxyAPI (The Gateway)

The Gateway bridges the CLI tools into a single API endpoint.

```bash
git clone https://github.com/router-for-me/CLIProxyAPI.git
cd CLIProxyAPI
pip install -r requirements.txt
python main.py  # Default port: 8317
```

---

## 3. jolly-flow (The Engine)

### Installation (Global Tool)
We recommend installing `jolly-flow` as a tool so it is available from any directory.

```bash
# Clone the repository
git clone https://github.com/thejollydev/jolly-flow.git
cd jolly-flow

# Install uv (modern package manager)
pip install uv

# Install jolly-flow as a global tool
uv tool install -e .
```

*Note: The `-e` flag allows you to edit the code and have changes take effect immediately.*

### ⚙️ Initial Setup
Run the interactive setup to configure your directories:

```bash
jolly-flow setup
```

---

## 4. Open WebUI (The Chat UI)

Deploy the container with access to your local files.

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

### Enable the Function
1. Open `http://localhost:3000`.
2. Navigate to **Admin Panel > Functions**.
3. Create a new function and paste the code from `src/jolly_flow/pipelines/jolly_pipeline.py`.
4. Save and Enable.

---

## 5. Observability (Optional)

Configure LangSmith to track agent performance.

```bash
jolly-flow config set-langsmith-key <YOUR_KEY>
```

