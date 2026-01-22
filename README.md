# The Jolly Method

> A subscription-first, LangGraph-orchestrated AI project framework for taking any idea from concept to execution.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## What is The Jolly Method?

The Jolly Method is a framework that helps you plan and execute projects using multiple AI models while:

✅ **Using your existing subscriptions** (Claude Pro, Google AI Pro)
✅ **Giving you control** over which AI model handles each task
✅ **Maintaining context** when switching between models
✅ **Keeping you in the loop** with human approval at every step

---

## Quick Start

### Prerequisites

- Python 3.11+
- Claude Pro subscription ($20/mo) - [Get it here](https://claude.ai/upgrade)
- Google AI Pro subscription ($19.99/mo) - [Get it here](https://one.google.com/about/google-ai-plans/)
- Docker (for Open WebUI)

### Installation

```bash
# 1. Install CLI tools
npm install -g @anthropic-ai/claude-code
npm install -g @google-ai/gemini-cli
curl -fsSL https://ollama.com/install.sh | sh

# 2. Install CLIProxyAPI
git clone https://github.com/router-for-me/CLIProxyAPI
cd CLIProxyAPI
python server.py  # Runs on localhost:8000

# 3. Install jolly-flow (coming soon in Phase 4)
# pip install jolly-flow

# 4. Install Open WebUI
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

### Configure Open WebUI

1. Open http://localhost:3000
2. Go to Settings → Connections
3. Add "OpenAI Compatible" provider:
   - Base URL: `http://localhost:8000/v1`
   - Add models: `claude-opus-4.5`, `gemini-3-pro`, `qwen2.5-coder`

### Configure Cline (VS Code)

1. Install the "Cline" extension
2. Open settings
3. Select "OpenAI Compatible" provider
4. Set Base URL: `http://localhost:8000/v1`

---

## Usage (When Ready)

```bash
# Create a new project
jolly-flow new-project "My Project Name" --type software

# Generate documentation with AI assistance
jolly-flow generate docs

# Sync files between Obsidian vault and project repo
jolly-flow sync
```

---

## How It Works

```
┌─────────────────────────────────────┐
│  Your Interfaces                     │
│  • Open WebUI (planning)            │
│  • Cline (coding)                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  CLIProxyAPI (localhost:8000)       │
│  • claude-code (your subscription)  │
│  • gemini-cli (your subscription)   │
│  • ollama (local, free)             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  jolly-flow (LangGraph)             │
│  • Manual model selection           │
│  • Context continuity               │
│  • Human-in-the-loop                │
└─────────────────────────────────────┘
```

You choose which AI model handles each task, and context automatically carries over when you switch models.

---

## Documentation

**User Guides:**
- [Installation](docs/installation.md) *(coming soon)*
- [Quick Start Tutorial](docs/quickstart.md) *(coming soon)*
- [Configuration](docs/configuration.md) *(coming soon)*

**Reference:**
- [CLI Commands](docs/cli-reference.md) *(coming soon)*
- [Templates](docs/templates.md) *(coming soon)*
- [Agents](docs/agents.md) *(coming soon)*

---

## Project Status

**Current Phase:** Phase 1 - Core Infrastructure Setup
**Progress:** Foundation complete, building CLI tool

See the private vault for detailed implementation roadmap.

---

## Features

- ✅ Use Claude Pro and Google AI Pro subscriptions (not pay-per-token APIs)
- ✅ Manual model selection to control quota usage
- ✅ Context continuity across model switches
- ✅ Human approval at every step
- ✅ Unified interface (Open WebUI, Cline)
- ✅ Local model support (Ollama)
- 🔄 Document template library *(in progress)*
- 🔄 LangGraph agent orchestration *(in progress)*
- ⏳ jolly-flow CLI tool *(Phase 4)*

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | LangGraph |
| Model Gateway | CLIProxyAPI |
| Planning UI | Open WebUI |
| Coding UI | Cline (VS Code) |
| CLI Tool | Python (Click/Typer) |
| Local Models | Ollama |

---

## Cost

**Fixed:** $40/month (Claude Pro + Google AI Pro)
**Variable:** $0 (everything else is free!)

---

## Contributing

This is a personal framework, but suggestions are welcome! Open an issue or PR.

---

## License

MIT License - See LICENSE file for details

---

## Author

Joseph - CS Student & Aspiring ML Engineer

Built with Claude Opus 4.5, Gemini 3 Pro, and lots of ☕

---

**🚀 Generated with The Jolly Method**
