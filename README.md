# jolly-flow

> **The Intelligent AI Project Orchestration Engine.**

`jolly-flow` is a production-grade CLI tool designed to transform abstract project ideas into comprehensive, actionable documentation using a multi-model agentic workflow. It leverages **LangGraph** for orchestration and **CLIProxyAPI** to utilize your existing AI subscriptions (Claude, Gemini, Ollama).

---

## ✨ Features

- **🤖 Autonomous Agents:** Specialized agents for Requirements Gathering, Architecture Design, and Roadmap Planning.
- **🔄 Subscription-First:** Built-in support for fixed-cost AI subscriptions via CLIProxyAPI.
- **💾 Context Persistence:** Maintains a unified `AI-CONTEXT.md` "baton" across model switches and sessions.
- **🏢 Enterprise-Ready Sync:** Automatically sanitizes and transforms Obsidian-flavored documentation into standard Markdown for Git repositories.
- **🐳 Web-Native:** Includes a self-bootstrapping integration for **Open WebUI**.
- **🔭 Deep Observability:** Integrated with **LangSmith** for real-time tracing and token usage tracking.

---

## 📚 Documentation

Detailed guides for every aspect of the system:

- **[Installation Guide](docs/installation.md):** Complete environment setup (CLI tools, Gateway, Docker).
- **[Workflow Guide](docs/workflow.md):** How to use the agents to plan a project.
- **[Open WebUI Integration](docs/open-webui.md):** How to use the chat interface to trigger agents.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/thejollydev/jolly-flow.git
cd jolly-flow

# Setup environment and install dependencies
pip install uv
uv sync
```

### 2. Scaffold a Project

```bash
uv run jolly-flow new-project "My Next Project"
```

### 3. Run the Agents

```bash
# Start the Requirements interview
uv run jolly-flow generate-requirements
```

*(Refer to the [Workflow Guide](docs/workflow.md) for the full end-to-end process.)*

---

## 🏗️ Project Structure

| File/Folder | Purpose |
|:---|:---|
| `src/jolly_flow` | Primary source code for the CLI and agents. |
| `docs/` | Comprehensive user and technical documentation. |
| `tests/` | Automated test suite. |
| `pyproject.toml` | Project metadata and dependency definitions. |
| `uv.lock` | **Crucial:** Pinpoint-accurate "fingerprint" of all dependencies to ensure the tool runs identically for every user. |
| `MANIFEST.in` | **Crucial:** Ensures non-Python files (like project templates) are included when the package is installed. |
| `LICENSE` | MIT Open Source license. |

---

## 🛠️ Architecture

`jolly-flow` follows a strict **Human-in-the-Loop** (HITL) pattern:
1.  **State Initialization:** Reads project context.
2.  **Agent Logic:** Generates documentation draft based on interactive input.
3.  **Human Review:** Pauses for user approval or revision requests.
4.  **Persistence:** Saves final artifacts and updates global context.

---

## 👨‍💻 Author

**Joseph** - *Software Engineering & AI Architecture*

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
