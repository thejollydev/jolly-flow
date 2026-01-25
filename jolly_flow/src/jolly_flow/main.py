import typer
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .sync.sync import sync_files
from .scaffold import create_project
from .agents.orchestrator import create_requirements_graph
from langchain_core.messages import HumanMessage

app = typer.Typer(help="The Jolly Method CLI")
console = Console()

@app.command()
def new_project(
    name: str = typer.Argument(..., help="Name of the project"),
    vault_root: str = typer.Option("/home/joseph/GoogleDrive/Obsidian/JollyProjects", help="Root directory for private vaults"),
    projects_root: str = typer.Option("/home/joseph/GoogleDrive/Projects", help="Root directory for public repositories"),
    templates_dir: str = typer.Option("/home/joseph/GoogleDrive/Obsidian/TheJollyMethod/templates", help="Directory containing Jinja2 templates")
):
    """Scaffolds a new project."""
    create_project(name, vault_root, projects_root, templates_dir)

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
    model: str = typer.Option("gemini-2.5-flash", help="Model ID to use")
):
    """Runs the requirements gathering agent."""
    # 1. Load context
    context_path = Path(project_path) / "AI-CONTEXT.md"
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found in {project_path}[/red]")
        return

    # 2. Setup Initial State
    initial_state = {
        "messages": [HumanMessage(content="Let's start the requirements gathering.")],
        "project_name": "Test Project",
        "project_path": project_path,
        "current_phase": "Phase 0",
        "instructions": ""
    }

    # 3. Run Graph
    graph = create_requirements_graph(model)
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
