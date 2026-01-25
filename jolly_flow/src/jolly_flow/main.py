import typer
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .sync.sync import sync_files
from .scaffold import create_project

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
