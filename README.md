# The Jolly Method

> A subscription-first, LangGraph-orchestrated AI project framework for taking any idea from concept to execution.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## What is The Jolly Method?

The Jolly Method is an opinionated framework for AI-assisted project planning and execution that:

✅ **Uses your existing subscriptions** (Claude Pro, Google AI Pro) through CLI tools
✅ **Gives you manual control** over which AI model handles each task
✅ **Maintains context continuity** when switching between models
✅ **Includes human oversight** at every step via LangGraph's human-in-the-loop
✅ **Provides unified interfaces** (Open WebUI, Cline) for all models

---

## Core Components

### jolly-flow CLI

The main orchestration tool that wraps LangGraph agents:

```bash
# Create a new project
jolly-flow new-project "My Project" --type software

# Generate documentation
jolly-flow generate docs --phase 1

# Sync files between Obsidian vault and project repo
jolly-flow sync
```

### CLIProxyAPI Integration

Wraps your subscription-based CLIs (claude-code, gemini-cli) and local models (ollama) as a unified OpenAI-compatible API:

- **claude-code** → Uses Claude Pro subscription
- **gemini-cli** → Uses Google AI Pro subscription
- **ollama** → Local models (free, unlimited)

### Multi-Interface Access

- **Open WebUI** - Web-based planning with conversation history and LangGraph pipelines
- **Cline** - VS Code extension for daily coding with AI assistance
- **AionUi** - Beautiful native UI for quick interactions (optional)

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Orchestration | **LangGraph** | Agent workflows with human-in-the-loop |
| Model Gateway | **CLIProxyAPI** | Unified API for all models |
| Planning Interface | **Open WebUI** | Web-based planning |
| Coding Interface | **Cline** | IDE integration |
| CLI Tool | **jolly-flow** | Custom Python CLI |
| Local Models | **Ollama** | Free fallback models |
| Observability | **LangSmith** | Agent tracking (free tier) |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Claude Pro subscription ($20/mo)
- Google AI Pro subscription ($19.99/mo)
- Docker (for Open WebUI)

### Installation

1. **Install CLI tools:**
   ```bash
   # Install claude-code CLI
   npm install -g @anthropic-ai/claude-code
   claude /login

   # Install gemini-cli
   npm install -g @google-ai/gemini-cli
   gemini-cli auth login

   # Install ollama
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull qwen2.5-coder:14b
   ```

2. **Install CLIProxyAPI:**
   ```bash
   git clone https://github.com/router-for-me/CLIProxyAPI
   cd CLIProxyAPI
   python server.py  # Runs on localhost:8000
   ```

3. **Install jolly-flow:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/the-jolly-method
   cd the-jolly-method
   pip install -e .
   ```

4. **Install Open WebUI:**
   ```bash
   docker run -d -p 3000:8080 \
     -v open-webui:/app/backend/data \
     --name open-webui \
     ghcr.io/open-webui/open-webui:main

   # Configure to use CLIProxyAPI at http://localhost:8000/v1
   ```

5. **Install Cline in VS Code:**
   - Open VS Code
   - Install "Cline" extension
   - Configure OpenAI Compatible provider: `http://localhost:8000/v1`

---

## Usage Example

```bash
# Start a new project
jolly-flow new-project "JollyLab K8s Cluster" --type infrastructure

# jolly-flow prompts:
# "Select model for Requirements Agent:"
# [1] Claude Opus 4.5 (75% quota remaining)
# [2] Gemini 3 Pro (100% quota remaining)
# [3] Ollama Qwen 2.5 Coder (Local - Free)
#
# You choose: 1

# Agent generates REQUIREMENTS.md
# Updates AI-CONTEXT.md
# Prompts for next agent...

# All documentation generated in:
# ~/GoogleDrive/Obsidian/JollyProjects/jollylab-k8s-cluster/

# Open in Cline for implementation:
code ~/projects/jollylab-k8s-cluster
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│ Your Interfaces                          │
│ • Open WebUI (planning)                 │
│ • Cline (coding)                        │
│ • AionUi (quick interactions)           │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ CLIProxyAPI (localhost:8000)            │
│ Wraps:                                  │
│ • claude-code (Claude Pro subscription) │
│ • gemini-cli (Google AI Pro)           │
│ • ollama (local models)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ jolly-flow (LangGraph Orchestration)    │
│ • Manual model selection                │
│ • Context continuity (AI-CONTEXT.md)    │
│ • Human-in-the-loop at every step       │
└─────────────────────────────────────────┘
```

---

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Creating Your First Project](docs/quickstart.md)
- [LangGraph Agents](docs/agents.md)
- [Templates Reference](docs/templates.md)

---

## Project Structure

```
the-jolly-method/
├── jolly-flow/              # Main CLI tool
│   ├── agents/              # LangGraph agent definitions
│   ├── cli/                 # CLI command implementations
│   ├── sync/                # File synchronization logic
│   └── templates/           # Document templates
├── docs/                    # Public documentation
├── tests/                   # Test suite
└── README.md                # This file
```

---

## Related Repositories

- **TheJollyMethod** - Private Obsidian vault with framework documentation
- **JollyProjects** - Private Obsidian vault with project planning docs

---

## Contributing

This is a personal framework, but suggestions are welcome! Open an issue or PR.

---

## License

MIT License - See LICENSE file for details

---

## Author

Joseph - CS Student & Aspiring ML Engineer

Built with Claude Opus 4.5, Gemini 3 Pro, and lots of coffee ☕

---

**🚀 Generated with The Jolly Method**
