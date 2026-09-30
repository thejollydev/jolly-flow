# The Jolly Method - Open WebUI Pipe Function

This is a **Pipe Function** (not a Pipeline server) that allows you to trigger `jolly-flow` agents directly from the Open WebUI chat interface.

## What is a Pipe Function?

Open WebUI Pipe Functions are Python code snippets that run directly within the Open WebUI process, allowing you to extend functionality through the web UI. This is different from Pipelines (which require a separate server).

**Key Features:**
- 🔌 Runs directly in Open WebUI (no separate server needed)
- 💬 Appears as a selectable "model" in the chat interface
- ⚡ Streams command output in real-time
- 🔧 Configurable via Valves (settings UI)

## Installation

### Step 1: Open the Functions UI

1. Access your Open WebUI instance at `http://localhost:3000`
2. Navigate to **Workspace** → **Functions** → **+** (Add Function button)

### Step 2: Add the Function

1. Copy the **entire contents** of `jolly_pipeline.py` (from this directory)
2. Paste into the code editor in Open WebUI
3. Click **Save**

### Step 3: Enable the Function

1. Find "The Jolly Method" in your functions list
2. Toggle the switch to **enable** it
3. (Optional) Click the gear icon to configure Valves if your paths differ from defaults

### Step 4: Configure Valves (Optional)

If your jolly-flow installation is in a different location:

1. Click the **gear icon** next to "The Jolly Method" function
2. Update the `jolly_path` setting to point to your `jolly-flow` executable
3. Update the `pythonpath` if your source directory differs
4. Click **Save**

**Default Settings:**
- `jolly_path`: `~/GoogleDrive/Projects/the-jolly-method/jolly_flow/.venv/bin/jolly-flow`
- `pythonpath`: `~/GoogleDrive/Projects/the-jolly-method/jolly_flow/src`

## Usage

### Select the Function

1. In the Open WebUI chat interface
2. Click the **model dropdown** at the top
3. Select **"The Jolly Method"**

### Available Commands

Send these commands in the chat:

#### Project Status
```
/status
```
Shows the current project phase and status from AI-CONTEXT.md

#### Synchronization
```
/sync
```
Synchronizes vault documents to the repository

```
/sync --dry-run
```
Preview what would be synced without making changes

#### Agent Workflows

```
/generate requirements
```
Start interactive requirements gathering with the Requirements Agent

```
/generate architecture
```
Start interactive architecture design with the Architect Agent

```
/generate roadmap
```
Start interactive roadmap planning with the Planner Agent

```
/start-phase 1
```
Generate detailed implementation guides for Phase 1 (or any phase number)

### Example Interaction

```
User: /status

The Jolly Method:
╭─────────────────────────────────────────╮
│ Project Status                          │
│ Current Phase: 6 - Additional Agents    │
│ Status: Complete                        │
│ Last Updated: 2026-01-25                │
╰─────────────────────────────────────────╯

User: /generate requirements

The Jolly Method:
🤖 Select Model for Requirements Agent
[1] claude-opus-4-5
[2] gemini-2.5-flash-lite
[3] qwen2.5-coder:14b

Select model (1-3) or press Enter for default:
```

## How It Works

1. **Command Routing:** The Pipe Function parses chat messages starting with `/`
2. **CLI Execution:** Executes the corresponding `jolly-flow` command as a subprocess
3. **Streaming Output:** Captures stdout and streams it back to the chat interface line-by-line
4. **Interactive Sessions:** Supports human-in-the-loop workflows where agents ask questions

## Troubleshooting

### Function doesn't appear in model list

- Ensure the function is **enabled** (toggle switch is on)
- Refresh the Open WebUI page
- Check browser console for errors

### "jolly-flow executable not found" error

- Click the gear icon to edit Valves
- Update `jolly_path` to the correct location
- Verify the path exists: `ls -la /path/to/jolly-flow`

### Commands hang or don't respond

- Check that Open WebUI has `ENABLE_TOOLS=true` environment variable
- Restart the Open WebUI container if needed
- Check Docker logs: `docker logs open-webui`

### Pydantic warnings

- These are cosmetic warnings from LangChain and can be safely ignored
- They don't affect functionality

## Architecture

```
┌─────────────────┐
│   Open WebUI    │
│   Chat UI       │
└────────┬────────┘
         │ /generate requirements
         ▼
┌─────────────────┐
│  Pipe Function  │  (jolly_pipeline.py)
│  - Parse command│
│  - Route to CLI │
└────────┬────────┘
         │ subprocess
         ▼
┌─────────────────┐
│  jolly-flow CLI │
│  - LangGraph    │
│  - Agents       │
│  - Models       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CLIProxyAPI    │  (localhost:8317)
│  - Claude       │
│  - Gemini       │
│  - Ollama       │
└─────────────────┘
```

## Security Note

⚠️ **Important:** Pipe Functions run arbitrary Python code within Open WebUI. Only install functions from sources you trust.

This function executes subprocess calls to `jolly-flow`, which in turn calls AI models. Ensure your Open WebUI instance is not publicly accessible unless properly secured.

## Requirements

- Open WebUI with `ENABLE_TOOLS=true`
- jolly-flow CLI installed and functional
- CLIProxyAPI running on localhost:8317
- Python packages: `pydantic`, `asyncio` (included in Open WebUI)

## Version

- **Open WebUI:** Latest (main branch)
- **jolly-flow:** 0.1.0
- **Pipe Function Version:** 1.0.0 (2026-01-25)

---

**Status:** Production Ready
**Last Updated:** 2026-01-25
**Maintained by:** The Jolly Method Framework
