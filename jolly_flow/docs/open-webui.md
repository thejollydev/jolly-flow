# Open WebUI Integration

The Jolly Method includes a powerful integration with **Open WebUI**, allowing you to chat with your project context and trigger agents from a web interface.

## How it Works (The "Brain in a Box")

Open WebUI runs in a Docker container. `jolly-flow` runs on your host machine. Normally, they can't talk to each other.

We solve this with a **Pipe Function**:
1.  **Volume Mount:** We mount your Google Drive into the container (`-v`).
2.  **Self-Installing Function:** The Pipe Function detects that `jolly-flow` is missing inside the container and automatically installs it from your mounted source code.
3.  **Command Routing:** When you type `/generate requirements`, the function intercepts it and runs the CLI command.

## Usage

### 1. Select the Model
In Open WebUI, click the model dropdown and select **"The Jolly Method"**.

### 2. Check Status
Type:
```
/status --project-path /home/joseph/GoogleDrive/Obsidian/JollyProjects/my-project
```

### 3. Run Agents
Type:
```
/generate requirements
```

**Note on Interactivity:**
Open WebUI does not support interactive prompts (stdin) yet. If an agent asks a question, the Pipe Function currently cannot capture your answer dynamically in the same way a terminal can.

**Recommended Workflow:**
- Use **Open WebUI** for status checks, syncing, and querying project docs.
- Use **Terminal** for the interactive Interview phases (`generate-*`).
