# The Jolly Method - System Architecture

**Version:** 1.0
**Last Updated:** 2026-01-21
**Status:** Design Finalized - Ready for Implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [System Components](#system-components)
4. [Data Flow](#data-flow)
5. [Integration Architecture](#integration-architecture)
6. [Deployment Model](#deployment-model)
7. [Security & Privacy](#security--privacy)

---

## Overview

The Jolly Method is a **subscription-first, LangGraph-orchestrated framework** for AI-assisted project planning and execution. It enables manual model selection, context continuity across model switches, and human oversight at every step.

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │ Open WebUI │  │Cline (IDE) │  │  AionUi    │             │
│  │(Planning)  │  │(Coding)    │  │(Optional)   │             │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘             │
└────────┼────────────────┼────────────────┼──────────────────┘
         │                │                │
         └────────────────┴────────────────┘
                          │
         ┌────────────────▼────────────────┐
         │       CLIProxyAPI                │
         │    (localhost:8000/v1)           │
         │                                  │
         │  Wraps:                         │
         │  • claude-code (Claude Pro)     │
         │  • gemini-cli (Google AI Pro)   │
         │  • ollama (local models)        │
         └────────────────┬────────────────┘
                          │
         ┌────────────────▼────────────────┐
         │     jolly-flow CLI               │
         │  (LangGraph Orchestration)       │
         │                                  │
         │  Agents:                         │
         │  • Requirements Analyst          │
         │  • System Architect              │
         │  • DevOps Engineer               │
         │  • Code Reviewer                 │
         └────────────────┬────────────────┘
                          │
         ┌────────────────▼────────────────┐
         │      Storage Layer               │
         │                                  │
         │  TheJollyMethod Vault (Private)  │
         │  JollyProjects Vault (Private)   │
         │  ~/Projects/{project}/ (Public)  │
         └──────────────────────────────────┘
```

---

## Core Principles

### 1. Subscription-First Billing

**Problem:** Pay-per-token API costs are prohibitive for heavy agentic workflows.

**Solution:** Leverage existing fixed-cost subscriptions:
- **Claude Pro** ($20/mo) → claude-code CLI
- **Google AI Pro** ($19.99/mo) → gemini-cli
- **Local models** (Free) → ollama

**Total cost:** $40/mo fixed, regardless of usage

### 2. Manual Model Selection

**Problem:** Pre-assigning models to agents can exhaust quotas for specific models.

**Solution:** Prompt user to select model for each agent invocation:

```
Select model for Requirements Agent:
[1] Claude Opus 4.5 (75% quota remaining) ✓
[2] Gemini 3 Pro (100% quota remaining)
[3] Ollama Qwen 2.5 Coder (Local - Free)

Your choice: _
```

### 3. Context Continuity

**Problem:** Switching models loses conversation context.

**Solution:** `AI-CONTEXT.md` acts as "the baton" passed between models:

```markdown
## Project: JollyLab K8s Cluster
**Last Updated:** 2026-01-21 14:30
**Current Phase:** Architecture Design
**Last Agent:** Requirements Analyst (Claude Opus 4.5)

## What's Been Done
- ✅ Requirements gathered

## Next Steps
1. Design system architecture
2. Create deployment plan

## Open Questions
- 3 nodes or 4 nodes?
```

Every agent:
1. Reads AI-CONTEXT.md FIRST
2. Processes its task
3. Updates AI-CONTEXT.md LAST

### 4. Human-in-the-Loop

LangGraph's built-in human approval nodes ensure you review and approve at every step:

```python
workflow = StateGraph(State)
workflow.add_node("requirements_agent", requirements_agent)
workflow.add_node("human_review", lambda s: s)  # Pause
workflow.add_edge("requirements_agent", "human_review")
workflow.add_conditional_edges("human_review", should_continue)
```

---

## System Components

### Component 1: CLIProxyAPI (Model Gateway)

**Repository:** https://github.com/router-for-me/CLIProxyAPI

**Purpose:** Wraps subscription-based CLIs and local models as unified OpenAI-compatible API

**Architecture:**
```
CLIProxyAPI Server (localhost:8000)
├── /v1/models               # List available models
├── /v1/chat/completions     # OpenAI-compatible chat endpoint
└── /v1/completions          # OpenAI-compatible completion endpoint

Backend Providers:
├── claude-code CLI          # Uses OAuth, Claude Pro subscription
├── gemini-cli               # Uses OAuth, Google AI Pro subscription
└── ollama                   # Local HTTP API
```

**Key Features:**
- Multi-account load balancing
- Round-robin selection
- Automatic failover
- No API keys required (uses CLI OAuth)

**Configuration:**
```yaml
# CLIProxyAPI config.yaml
providers:
  - name: claude-opus-4.5
    cli: claude-code
    model: claude-opus-4-5
  - name: gemini-3-pro
    cli: gemini-cli
    model: gemini-3-pro
  - name: qwen2.5-coder-14b
    cli: ollama
    model: qwen2.5-coder:14b
```

### Component 2: jolly-flow CLI (Orchestration)

**Location:** `~/GoogleDrive/Projects/the-jolly-method/jolly-flow/`

**Purpose:** Custom Python CLI that wraps LangGraph agents

**Architecture:**
```
jolly-flow/
├── cli/
│   ├── __init__.py
│   ├── new_project.py       # jolly-flow new-project
│   ├── generate.py          # jolly-flow generate docs
│   └── sync.py              # jolly-flow sync
├── agents/
│   ├── base_agent.py        # Common agent logic
│   ├── requirements_agent.py
│   ├── architect_agent.py
│   ├── devops_agent.py
│   └── reviewer_agent.py
├── sync/
│   └── file_sync.py         # jolly-sync logic
└── templates/
    ├── project_overview.md.j2
    ├── architecture.md.j2
    └── ...
```

**Key Features:**
- Click/Typer-based CLI framework
- LangGraph agent orchestration
- Template rendering (Jinja2)
- File synchronization
- Model selection prompts
- Usage tracking

**Example Flow:**
```bash
$ jolly-flow generate docs --project jollylab

# Internally:
1. Load project config from JollyProjects/jollylab/
2. Read AI-CONTEXT.md
3. For each agent:
   a. Prompt user for model selection
   b. Call CLIProxyAPI with chosen model
   c. Run LangGraph agent
   d. Save output to JollyProjects/jollylab/
   e. Update AI-CONTEXT.md
   f. Pause for human review
4. Complete workflow
```

### Component 3: Open WebUI (Planning Interface)

**Repository:** https://github.com/open-webui/open-webui

**Purpose:** Web-based chat interface with LangGraph pipeline integration

**Integration:**
```
Open WebUI (localhost:3000)
├── Settings → Connections
│   └── Add OpenAI Compatible
│       ├── Base URL: http://localhost:8000/v1
│       └── Models: [claude-opus-4.5, gemini-3-pro, ...]
│
└── Pipelines
    └── Custom Pipeline: jolly-flow-pipeline
        ├── Invokes: jolly-flow CLI commands
        ├── Streams: Agent output to chat
        └── Handles: Model selection via UI prompts
```

**Features:**
- Conversation history
- Model switching within conversation
- Markdown rendering
- File uploads
- Custom pipelines for jolly-flow

### Component 4: Cline (Coding Interface)

**Repository:** https://github.com/cline/cline

**Purpose:** VS Code extension for AI-assisted coding with file access

**Configuration:**
```json
{
  "cline.apiProvider": "openai-compatible",
  "cline.openaiCompatible.baseUrl": "http://localhost:8000/v1",
  "cline.openaiCompatible.apiKey": "dummy",
  "cline.openaiCompatible.models": [
    "claude-opus-4.5",
    "gemini-3-pro",
    "qwen2.5-coder-14b"
  ]
}
```

**Features:**
- File system access (Obsidian vaults + project folders)
- Terminal integration
- Multi-file editing
- Manual model switching

### Component 5: LangGraph Agents

**Framework:** https://github.com/langchain-ai/langgraph

**Agent Definition Example:**
```python
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

class RequirementsAgent:
    def __init__(self, model_choice):
        self.llm = ChatOpenAI(
            base_url="http://localhost:8000/v1",
            model=model_choice,
            api_key="dummy"
        )

    def run(self, state):
        # Read AI-CONTEXT.md
        context = self.read_context(state["project_path"])

        # Generate requirements
        prompt = self.build_prompt(state["project_name"], context)
        response = self.llm.invoke(prompt)

        # Save to REQUIREMENTS.md
        self.save_output(state["project_path"], response)

        # Update AI-CONTEXT.md
        self.update_context(state["project_path"], response)

        return state
```

**Workflow Example:**
```python
workflow = StateGraph(State)

# Add nodes
workflow.add_node("requirements_agent", requirements_agent)
workflow.add_node("human_review_requirements", lambda s: s)
workflow.add_node("architect_agent", architect_agent)
workflow.add_node("human_review_architecture", lambda s: s)

# Add edges
workflow.add_edge("requirements_agent", "human_review_requirements")
workflow.add_conditional_edges(
    "human_review_requirements",
    should_continue,  # User approves or rejects
    {
        "continue": "architect_agent",
        "revise": "requirements_agent"
    }
)
```

### Component 6: Storage Layer

**Structure:**
```
/home/joseph/GoogleDrive/Obsidian/
├── TheJollyMethod/          # Framework knowledge base (private git repo)
│   ├── templates/           # Master templates
│   ├── prompts/             # Prompt library
│   ├── agents/              # Agent configs
│   ├── standards/           # Global standards
│   └── guides/              # Usage guides
│
├── JollyProjects/           # All project planning (private git repo)
│   ├── jollylab/
│   │   ├── PROJECT-OVERVIEW.md
│   │   ├── ARCHITECTURE.md
│   │   ├── ROADMAP.md
│   │   ├── AI-CONTEXT.md
│   │   ├── phases/
│   │   └── journal/
│   └── brewery-app/
│
└── ai-vault/                # Temporary (archive after migration)

/home/joseph/GoogleDrive/Projects/
├── the-jolly-method/        # Framework code (public git repo)
│   ├── jolly-flow/
│   ├── docs/
│   └── tests/
│
├── jollylab/                # JollyLab code (public git repo)
│   ├── terraform/
│   ├── k8s/
│   └── README.md            # Synced from JollyProjects/jollylab/
│
└── brewery-app/             # BezaCore project (public git repo)
```

---

## Data Flow

### Workflow: Creating a New Project

```
1. User runs: jolly-flow new-project "JollyLab K8s Cluster"

2. jolly-flow CLI:
   ├── Creates JollyProjects/jollylab/ directory
   ├── Copies templates from TheJollyMethod/templates/
   ├── Replaces {{PROJECT_NAME}} with "JollyLab K8s Cluster"
   ├── Creates ~/Projects/jollylab/ directory
   ├── Initializes both git repos
   └── Creates .jolly-sync.yaml

3. User runs: jolly-flow generate docs

4. jolly-flow orchestrates agents:
   ├── Prompts: "Select model for Requirements Agent"
   ├── User chooses: Claude Opus 4.5
   ├── Agent runs:
   │   ├── Calls CLIProxyAPI: POST /v1/chat/completions
   │   ├── CLIProxyAPI routes to claude-code CLI
   │   ├── Returns response
   │   ├── Saves to JollyProjects/jollylab/REQUIREMENTS.md
   │   └── Updates AI-CONTEXT.md
   ├── Pauses for human review
   ├── User approves
   ├── Prompts: "Select model for Architect Agent"
   ├── User chooses: Gemini 3 Pro (save Claude quota)
   ├── Agent reads AI-CONTEXT.md (context continuity!)
   ├── Generates ARCHITECTURE.md with Mermaid diagrams
   └── Repeats for all agents...

5. User runs: jolly-flow sync

6. jolly-sync:
   ├── Reads .jolly-sync.yaml
   ├── Copies README from vault → project repo
   ├── Transforms [[wikilinks]] to plain text
   ├── Removes Obsidian frontmatter
   └── Excludes private files (roadmaps, journals)

7. User commits to git:
   ├── cd ~/Projects/jollylab
   ├── git add .
   ├── git commit -m "Initial documentation from jolly-flow"
   └── git push origin main
```

### Context Continuity Across Model Switches

```
Agent 1 (Claude Opus 4.5):
├── Read: AI-CONTEXT.md (empty for first agent)
├── Generate: REQUIREMENTS.md
└── Update: AI-CONTEXT.md
    └── "Requirements complete. Next: Design architecture."

Agent 2 (Gemini 3 Pro):
├── Read: AI-CONTEXT.md (sees what Claude did!)
├── Generate: ARCHITECTURE.md based on requirements
└── Update: AI-CONTEXT.md
    └── "Architecture designed. Next: Infrastructure plan."

Agent 3 (Ollama Qwen):
├── Read: AI-CONTEXT.md (sees full history)
├── Generate: DEPLOYMENT.md
└── Update: AI-CONTEXT.md
    └── "Deployment plan complete. Ready for implementation."
```

---

## Integration Architecture

### jolly-flow ↔ CLIProxyAPI

```python
# jolly-flow calls CLIProxyAPI
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8000/v1",
    model=user_selected_model,  # "claude-opus-4.5" or "gemini-3-pro"
    api_key="dummy"
)

response = llm.invoke("Generate project requirements for...")
```

### Open WebUI ↔ jolly-flow

```python
# Open WebUI custom pipeline
from typing import Iterator

class JollyFlowPipeline:
    async def pipe(self, user_message: str, model_id: str) -> Iterator[str]:
        # Run jolly-flow command
        process = await asyncio.create_subprocess_exec(
            "jolly-flow", "generate", "docs",
            stdout=asyncio.subprocess.PIPE
        )

        # Stream output to Open WebUI chat
        async for line in process.stdout:
            yield line.decode()
```

### Cline ↔ Obsidian Vaults

```
Cline Workspace:
├── Open: ~/Projects/jollylab (code)
└── Open: ~/GoogleDrive/Obsidian/JollyProjects/jollylab (docs)

Cline can:
- Read from both locations
- Edit files in both locations
- Terminal access to run jolly-flow commands
```

---

## Deployment Model

### Development (Current)

**Environment:** Local laptop/desktop

**Components:**
- CLIProxyAPI: `localhost:8000`
- Open WebUI: `localhost:3000` (Docker)
- Cline: VS Code extension
- Ollama: `localhost:11434`
- jolly-flow: Installed via `pip install -e .`

### Homelab (Future - Optional)

**Environment:** Proxmox homelab (JollyProx)

**Components:**
- CLIProxyAPI: Docker container, accessible on LAN
- Open WebUI: Docker container with GPU pass-through for Ollama
- Ollama: Larger models on homelab GPU (RTX 3090)
- jolly-flow: Installed on homelab, accessible via SSH

**Benefits:**
- Larger local models (70B+ on homelab GPU)
- Access from any device on LAN
- Centralized agent orchestration

---

## Security & Privacy

### Subscription Credentials

**Storage:**
- claude-code OAuth tokens: `~/.claude/` (encrypted by CLI)
- gemini-cli OAuth tokens: `~/.gemini/` (encrypted by CLI)
- Never exposed to CLIProxyAPI or jolly-flow

**Access:**
- CLIProxyAPI spawns CLI subprocesses
- CLIs handle authentication internally
- No manual token management

### Private vs Public Data

**Private (Never leaves machine):**
- TheJollyMethod vault
- JollyProjects vault
- AI-CONTEXT.md
- Roadmaps, journals, implementation guides

**Public (Safe to push to GitHub):**
- the-jolly-method code repository
- Project code repositories (~/Projects/*)
- Public README, architecture overviews, user guides

**jolly-sync ensures this boundary is maintained**

### API Keys

**LangSmith (Optional):**
- Stored in environment variable: `LANGSMITH_API_KEY`
- Only for observability (can be skipped)
- Free tier: 5,000 traces/month

**No other API keys required** - subscriptions handle authentication

---

## Technology Stack Summary

| Layer | Technology | License | Cost |
|-------|-----------|---------|------|
| Orchestration | LangGraph | MIT | Free |
| CLI Framework | Click/Typer | BSD | Free |
| Model Gateway | CLIProxyAPI | MIT | Free |
| Planning UI | Open WebUI | MIT | Free |
| Coding UI | Cline | Apache 2.0 | Free |
| Local Models | Ollama | MIT | Free |
| Templates | Jinja2 | BSD | Free |
| Observability | LangSmith | Proprietary | Free tier |
| **Subscriptions** | **Claude Pro** | **Proprietary** | **$20/mo** |
| | **Google AI Pro** | **Proprietary** | **$19.99/mo** |

**Total Cost:** $40/mo fixed

---

## Architecture Decisions

### ADR-001: Subscription-First Model

**Context:** Pay-per-token API costs prohibitive for heavy use

**Decision:** Use claude-code and gemini-cli with subscription auth

**Consequences:**
- ✅ Fixed monthly cost
- ✅ No surprise bills
- ⚠️ Quota limits (but trackable)

### ADR-002: Manual Model Selection

**Context:** Pre-assigned models can exhaust quotas

**Decision:** Prompt user to choose model per agent

**Consequences:**
- ✅ Quota control
- ✅ User awareness of usage
- ⚠️ Slightly slower (requires user input)

### ADR-003: CLIProxyAPI as Gateway

**Context:** Need unified API for multiple CLI tools

**Decision:** Use CLIProxyAPI to wrap all CLIs

**Consequences:**
- ✅ OpenAI-compatible API
- ✅ Works with all LangChain tools
- ✅ Multi-account load balancing
- ⚠️ Extra dependency

### ADR-004: LangGraph (Not CrewAI)

**Context:** Need human-in-the-loop orchestration

**Decision:** Use LangGraph for transparency and control

**Consequences:**
- ✅ Full control over agent execution
- ✅ Human approval at every step
- ✅ State persistence
- ⚠️ More code than CrewAI

### ADR-005: Open WebUI (Not LM Studio)

**Context:** Need web interface for planning

**Decision:** Use Open WebUI for multi-model + Ollama support

**Consequences:**
- ✅ Ollama integration
- ✅ API provider support
- ✅ LangGraph pipeline integration
- ⚠️ Docker dependency

---

**Architecture Status:** ✅ Finalized - Ready for Implementation

**Next Steps:** Begin Phase 1 - Core Infrastructure Setup
