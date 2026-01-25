# The Jolly Method - Open WebUI Pipeline

This pipeline allows you to trigger `jolly-flow` agents directly from the Open WebUI chat interface.

## Installation

1.  **Requirement:** Your Open WebUI instance must have access to the `jolly-flow` Python environment and the Obsidian vaults.
2.  **Add Function:**
    - Go to **Workspace** -> **Functions** -> **+**.
    - Copy and paste the contents of `jolly_pipeline.py`.
    - Click **Save**.

## Usage

Select **The Jolly Method** from the model dropdown and use the following commands:

- `/status`: Show current project phase.
- `/generate requirements`: Start interactive requirements gathering.
- `/generate architecture`: Start interactive architecture design.
- `/sync`: Synchronize vault docs to the repo.
