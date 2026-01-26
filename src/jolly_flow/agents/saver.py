"""Save node for persisting agent outputs and updating AI-CONTEXT.md"""
from rich.console import Console
from .state import ProjectState
from .file_ops import save_requirements, save_architecture, save_roadmap, save_phase_guides, update_ai_context

console = Console()


def extract_document_content(messages) -> str:
    """Extract the generated document from agent messages.

    Args:
        messages: List of messages from the conversation

    Returns:
        The generated document content
    """
    # Find the last assistant message that contains substantial content
    for msg in reversed(messages):
        if hasattr(msg, 'content') and len(msg.content) > 200:
            return msg.content
    return ""


def save_requirements_node(state: ProjectState):
    """Save REQUIREMENTS.md and update AI-CONTEXT.md"""
    project_path = state["project_path"]
    content = extract_document_content(state["messages"])

    if not content:
        console.print("[yellow]⚠️  No content to save[/yellow]")
        return state

    # Save REQUIREMENTS.md
    if save_requirements(project_path, content):
        console.print(f"[green]✅ Saved: {project_path}/REQUIREMENTS.md[/green]")
    else:
        console.print("[red]❌ Failed to save REQUIREMENTS.md[/red]")
        return state

    # Update AI-CONTEXT.md
    summary = "Generated requirements document with functional and non-functional requirements"
    if update_ai_context(project_path, "Requirements", summary):
        console.print(f"[green]✅ Updated: {project_path}/AI-CONTEXT.md[/green]")
    else:
        console.print("[yellow]⚠️  Failed to update AI-CONTEXT.md[/yellow]")

    return state


def save_architecture_node(state: ProjectState):
    """Save ARCHITECTURE.md and update AI-CONTEXT.md"""
    project_path = state["project_path"]
    content = extract_document_content(state["messages"])

    if not content:
        console.print("[yellow]⚠️  No content to save[/yellow]")
        return state

    # Save ARCHITECTURE.md
    if save_architecture(project_path, content):
        console.print(f"[green]✅ Saved: {project_path}/ARCHITECTURE.md[/green]")
    else:
        console.print("[red]❌ Failed to save ARCHITECTURE.md[/red]")
        return state

    # Update AI-CONTEXT.md
    summary = "Generated architecture document with system design and diagrams"
    if update_ai_context(project_path, "Architecture", summary):
        console.print(f"[green]✅ Updated: {project_path}/AI-CONTEXT.md[/green]")
    else:
        console.print("[yellow]⚠️  Failed to update AI-CONTEXT.md[/yellow]")

    return state


def save_roadmap_node(state: ProjectState):
    """Save ROADMAP.md and update AI-CONTEXT.md"""
    project_path = state["project_path"]
    content = extract_document_content(state["messages"])

    if not content:
        console.print("[yellow]⚠️  No content to save[/yellow]")
        return state

    # Save ROADMAP.md
    if save_roadmap(project_path, content):
        console.print(f"[green]✅ Saved: {project_path}/ROADMAP.md[/green]")
    else:
        console.print("[red]❌ Failed to save ROADMAP.md[/red]")
        return state

    # Update AI-CONTEXT.md
    summary = "Generated roadmap with phase-based implementation plan"
    if update_ai_context(project_path, "Roadmap", summary):
        console.print(f"[green]✅ Updated: {project_path}/AI-CONTEXT.md[/green]")
    else:
        console.print("[yellow]⚠️  Failed to update AI-CONTEXT.md[/yellow]")

    return state


def save_phase_guide_node(state: ProjectState):
    """Save phase guide files (overview, checklist, implementation-guide) and update AI-CONTEXT.md"""
    project_path = state["project_path"]
    phase = state.get("current_phase", "1")
    content = extract_document_content(state["messages"])

    if not content:
        console.print("[yellow]⚠️  No content to save[/yellow]")
        return state

    # Save phase guides (3 files)
    if save_phase_guides(project_path, phase, content):
        console.print(f"[green]✅ Saved: {project_path}/phases/phase-{phase}/overview.md[/green]")
        console.print(f"[green]✅ Saved: {project_path}/phases/phase-{phase}/checklist.md[/green]")
        console.print(f"[green]✅ Saved: {project_path}/phases/phase-{phase}/implementation-guide.md[/green]")
    else:
        console.print("[red]❌ Failed to save phase guides[/red]")
        return state

    # Update AI-CONTEXT.md
    summary = f"Generated Phase {phase} implementation guides (overview, checklist, implementation guide)"
    if update_ai_context(project_path, f"Phase {phase} Guide", summary):
        console.print(f"[green]✅ Updated: {project_path}/AI-CONTEXT.md[/green]")
    else:
        console.print("[yellow]⚠️  Failed to update AI-CONTEXT.md[/yellow]")

    return state
