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


def save_phase_guides(project_path: str, phase: str, content: str) -> bool:
    """Save phase guide files (overview, checklist, implementation-guide).

    Args:
        project_path: Path to the project vault
        phase: Phase number (e.g., "1", "2")
        content: Content with ---FILE_SEPARATOR--- markers

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create phases directory if it doesn't exist
        phases_dir = Path(project_path) / "phases" / f"phase-{phase}"
        phases_dir.mkdir(parents=True, exist_ok=True)

        # Split content by separator
        parts = content.split("---FILE_SEPARATOR---")

        if len(parts) < 3:
            print(f"Warning: Expected 3 parts, got {len(parts)}")
            # Try to save what we have
            if len(parts) >= 1:
                overview_path = phases_dir / "overview.md"
                with open(overview_path, "w") as f:
                    f.write(parts[0].strip())
            if len(parts) >= 2:
                checklist_path = phases_dir / "checklist.md"
                with open(checklist_path, "w") as f:
                    f.write(parts[1].strip())
            if len(parts) >= 3:
                guide_path = phases_dir / "implementation-guide.md"
                with open(guide_path, "w") as f:
                    f.write(parts[2].strip())
            return True

        # Save all three files
        overview_path = phases_dir / "overview.md"
        checklist_path = phases_dir / "checklist.md"
        guide_path = phases_dir / "implementation-guide.md"

        with open(overview_path, "w") as f:
            f.write(parts[0].strip())
        with open(checklist_path, "w") as f:
            f.write(parts[1].strip())
        with open(guide_path, "w") as f:
            f.write(parts[2].strip())

        return True
    except Exception as e:
        print(f"Error saving phase guides: {e}")
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
