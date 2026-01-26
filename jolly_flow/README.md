# jolly-flow CLI

The orchestration engine for **The Jolly Method**.

`jolly-flow` is a Python CLI tool that manages the lifecycle of AI-driven project planning. It uses **LangGraph** to orchestrate agents (Requirements, Architect, Planner) and connects to LLMs via **CLIProxyAPI**.

## Features

*   **🤖 AI Agents:** Specialized agents for interviewing users and generating documentation.
*   **💾 Context Aware:** Agents read `AI-CONTEXT.md` to maintain state across sessions.
*   **🔄 Sync:** Seamlessly transforms Obsidian-flavored markdown into standard Git-ready markdown.
*   **🐳 Docker Ready:** Includes a self-installing Pipe Function for Open WebUI integration.
*   **🔭 Observable:** Built-in integration with LangSmith for tracing and cost tracking.

## Installation

### Prerequisites
*   Python 3.11 or higher
*   [uv](https://github.com/astral-sh/uv) (Recommended) or pip

### Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd jolly_flow

# Install with uv (creates venv automatically)
uv pip install -e .

# Or with standard pip
pip install -e .
```

## Usage

### Basic Commands

```bash
# Create a new project structure
jolly-flow new-project "My New App"

# Check project status
jolly-flow status --project-path /path/to/project

# Sync files from Vault to Repo
jolly-flow sync --project-path /path/to/project
```

### Agent Commands

```bash
# Start the Requirements Interview
jolly-flow generate-requirements

# Design the System Architecture
jolly-flow generate-architecture

# Create the Implementation Roadmap
jolly-flow generate-roadmap

# Generate Guides for a specific phase
jolly-flow start-phase 1
```

### Configuration

To enable LangSmith observability:

```bash
jolly-flow config set-langsmith-key <YOUR_API_KEY>
```

## Architecture

`jolly-flow` uses a **Human-in-the-loop** workflow:
1.  **Agent** generates content using an LLM.
2.  **Human** reviews the content in the terminal.
3.  **Approval** saves the file; **Revision** sends feedback back to the agent.

## Open WebUI Integration

To use `jolly-flow` from within Open WebUI:
1.  Enable "Functions" in Open WebUI.
2.  Copy the code from `src/jolly_flow/pipelines/jolly_pipeline.py`.
3.  Create a new Function in Open WebUI and paste the code.
4.  Ensure your Docker container mounts the project directory.

## License

MIT
