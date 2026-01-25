"""File operations for saving agent outputs and updating AI-CONTEXT.md"""
from pathlib import Path
from datetime import datetime
import re


def save_requirements(project_path: str, content: str) -> bool:
    """Save REQUIREMENTS.md to the project vault.

    Args:
        project_path: Path to the project vault
        content: Content to save

    Returns:
        True if successful, False otherwise
    """
    try:
        req_path = Path(project_path) / "REQUIREMENTS.md"
        with open(req_path, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving REQUIREMENTS.md: {e}")
        return False


def save_architecture(project_path: str, content: str) -> bool:
    """Save ARCHITECTURE.md to the project vault.

    Args:
        project_path: Path to the project vault
        content: Content to save

    Returns:
        True if successful, False otherwise
    """
    try:
        arch_path = Path(project_path) / "ARCHITECTURE.md"
        with open(arch_path, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving ARCHITECTURE.md: {e}")
        return False


def save_roadmap(project_path: str, content: str) -> bool:
    """Save ROADMAP.md to the project vault.

    Args:
        project_path: Path to the project vault
        content: Content to save

    Returns:
        True if successful, False otherwise
    """
    try:
        roadmap_path = Path(project_path) / "ROADMAP.md"
        with open(roadmap_path, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving ROADMAP.md: {e}")
        return False


def update_ai_context(project_path: str, agent_name: str, summary: str) -> bool:
    """Update AI-CONTEXT.md after agent completion.

    Updates the "What's Been Accomplished" section and adds a timestamp.

    Args:
        project_path: Path to the project vault
        agent_name: Name of the agent that completed (e.g., "Requirements", "Architecture")
        summary: Brief summary of what was accomplished

    Returns:
        True if successful, False otherwise
    """
    try:
        context_path = Path(project_path) / "AI-CONTEXT.md"

        if not context_path.exists():
            print(f"Error: AI-CONTEXT.md not found at {context_path}")
            return False

        # Read current content
        with open(context_path, "r") as f:
            content = f.read()

        # Update Last Updated timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = re.sub(
            r"\*\*Last Updated:\*\* .*",
            f"**Last Updated:** {now}",
            content
        )

        # Add to "What's Been Accomplished" section
        accomplishment = f"- {agent_name} agent completed: {summary} ({now})"

        # Find the section and add our accomplishment
        if "## What's Been Accomplished" in content:
            # Replace the placeholder or add to existing list
            if "*Agents will update this section after completing tasks*" in content:
                content = content.replace(
                    "*Agents will update this section after completing tasks*",
                    accomplishment
                )
            else:
                # Add after the section header
                content = re.sub(
                    r"(## What's Been Accomplished\n\n)",
                    f"\\1{accomplishment}\n",
                    content
                )

        # Write back
        with open(context_path, "w") as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"Error updating AI-CONTEXT.md: {e}")
        return False
