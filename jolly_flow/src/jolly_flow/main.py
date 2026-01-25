import typer
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .sync.sync import sync_files
from .scaffold import create_project
from .agents.orchestrator import create_requirements_graph, create_architecture_graph, create_roadmap_graph, create_phase_guide_graph
from .model_selector import select_model_interactive
from langchain_core.messages import HumanMessage

app = typer.Typer(help="The Jolly Method CLI")
console = Console()

@app.command()
def new_project(
    name: str = typer.Argument(..., help="Name of the project"),
    vault_root: str = typer.Option("/home/joseph/GoogleDrive/Obsidian/JollyProjects", help="Root directory for private vaults"),
    projects_root: str = typer.Option("/home/joseph/GoogleDrive/Projects", help="Root directory for public repositories")
):
    """Scaffolds a new project."""
    create_project(name, vault_root, projects_root)

@app.command()
def sync(
    config: str = typer.Option(".jolly-sync.yaml", help="Path to the config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen without making changes")
):
    """Syncs docs from vault to repo."""
    sync_files(config, dry_run)

@app.command()
def generate_requirements(
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Runs the Requirements Agent (Phase 0)."""
    # Use interactive selection if model not specified
    if model is None:
        model = select_model_interactive("Requirements")
    run_agent_workflow(project_path, model, create_requirements_graph, "Requirements")

@app.command()
def generate_architecture(
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Runs the Architect Agent (Phase 0)."""
    # Use interactive selection if model not specified
    if model is None:
        model = select_model_interactive("Architecture")
    run_agent_workflow(project_path, model, create_architecture_graph, "Architecture")

@app.command()
def generate_roadmap(
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Runs the Planner Agent (Phase 0)."""
    # Use interactive selection if model not specified
    if model is None:
        model = select_model_interactive("Roadmap")
    run_agent_workflow(project_path, model, create_roadmap_graph, "Roadmap")

@app.command()
def start_phase(
    phase: str = typer.Argument(..., help="Phase number to start"),
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Generates detailed guides for a specific phase."""
    # Use interactive selection if model not specified
    if model is None:
        model = select_model_interactive(f"Phase {phase} Guide")
    run_agent_workflow(project_path, model, create_phase_guide_graph, f"Phase {phase} Guide", phase)

def run_agent_workflow(project_path: str, model: str, graph_factory, agent_name: str, phase: str = "0"):
    # 1. Load context
    context_path = Path(project_path) / "AI-CONTEXT.md"
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found in {project_path}[/red]")
        return

    # 2. Read AI-CONTEXT.md for context continuity
    with open(context_path, "r") as f:
        ai_context = f.read()

    console.print(f"[dim]📖 Loaded AI-CONTEXT.md ({len(ai_context)} chars)[/dim]")

    # 3. Setup Initial State
    initial_state = {
        "messages": [HumanMessage(content=f"Let's generate the {agent_name}.")],
        "project_name": "Unknown",
        "project_path": project_path,
        "templates_dir": "",
        "current_phase": phase,
        "instructions": "",
        "ai_context": ai_context
    }

    # 4. Run Graph
    graph = graph_factory(model)
    for output in graph.stream(initial_state):
        for key, value in output.items():
            if key == "agent":
                console.print(f"\n[bold green]🤖 Agent:[/bold green] {value['messages'][-1].content}")

@app.command()
def status(project_path: str = typer.Option(".", help="Path to the project vault or repo")):
    """Shows current project status from AI-CONTEXT.md."""
    context_path = Path(project_path) / "AI-CONTEXT.md"
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found in {project_path}[/red]")
        return

    with open(context_path, "r") as f:
        content = f.read()

    phase_match = re.search(r"\*\*Current Phase:\*\* (.*)", content)
    status_match = re.search(r"- Status: (.*)", content)

    phase = phase_match.group(1) if phase_match else "Unknown"
    status = status_match.group(1) if status_match else "Unknown"

    table = Table(title="Project Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Phase", phase)
    table.add_row("Status", status)

    console.print(table)

if __name__ == "__main__":
    app()
