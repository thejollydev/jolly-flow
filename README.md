# jolly-flow CLI

The orchestration engine for **The Jolly Method**.

`jolly-flow` is a Python CLI tool that manages the lifecycle of AI-driven project planning. It uses **LangGraph** to orchestrate agents (Requirements, Architect, Planner) and connects to LLMs via **CLIProxyAPI**.

## 📚 Documentation

*   **[Installation Guide](docs/installation.md):** Setup CLIProxyAPI, Docker, and Tools.
*   **[Workflow Guide](docs/workflow.md):** How to use the agents to plan a project.
*   **[Open WebUI Integration](docs/open-webui.md):** Chat interface details.

## Features

*   **🤖 AI Agents:** Specialized agents for interviewing users and generating documentation.
*   **💾 Context Aware:** Agents read `AI-CONTEXT.md` to maintain state across sessions.
*   **🔄 Sync:** Seamlessly transforms Obsidian-flavored markdown into standard Git-ready markdown.
*   **🐳 Docker Ready:** Includes a self-installing Pipe Function for Open WebUI integration.
*   **🔭 Observable:** Built-in integration with LangSmith for tracing and cost tracking.

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/thejollydev/the-jolly-method.git
cd the-jolly-method/jolly_flow

# Install with uv
uv pip install -e .
```

### 2. Scaffold

```bash
jolly-flow new-project "My New App"
```

### 3. Plan

```bash
jolly-flow generate-requirements
```

*(See [Workflow Guide](docs/workflow.md) for the full process)*

## Architecture

`jolly-flow` uses a **Human-in-the-loop** workflow:
1.  **Agent** generates content using an LLM.
2.  **Human** reviews the content in the terminal.
3.  **Approval** saves the file; **Revision** sends feedback back to the agent.

## License

MIT
