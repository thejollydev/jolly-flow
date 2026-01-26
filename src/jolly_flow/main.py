import typer
import re
import os
import uuid
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from .sync.sync import sync_files
from .scaffold import create_project
from .agents.orchestrator import create_requirements_graph, create_architecture_graph, create_roadmap_graph, create_phase_guide_graph
from .model_selector import select_model_interactive
from .config_manager import ConfigManager
from .reporter import print_token_usage
from langchain_core.messages import HumanMessage

# --- Environment Setup ---
def configure_environment():
    """Injects API keys from config into environment variables."""
    langsmith_key = ConfigManager.get_key("langsmith_api_key")
    if langsmith_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = langsmith_key
        os.environ["LANGCHAIN_PROJECT"] = "jolly-flow"
        
        workspace_id = ConfigManager.get_key("langsmith_workspace_id")
        if workspace_id:
            os.environ["LANGSMITH_WORKSPACE_ID"] = workspace_id

configure_environment()

app = typer.Typer(help="jolly-flow: Intelligent AI Project Orchestration")
config_app = typer.Typer(help="Manage configuration and API keys")
app.add_typer(config_app, name="config")

console = Console()

# --- Helpers ---
def resolve_project_path(path_or_name: str) -> Path:
    """
    Resolves a project path. 
    1. Checks if it's a valid local path.
    2. If not, checks if it's a project name in the configured vault_root.
    """
    path = Path(path_or_name)
    
    # If path exists and has context, use it
    if (path / "AI-CONTEXT.md").exists():
        return path.absolute()
    
    # If not, check the vault_root
    vault_root = Path(ConfigManager.get_vault_root())
    vault_project_path = vault_root / path_or_name
    
    if (vault_project_path / "AI-CONTEXT.md").exists():
        return vault_project_path.absolute()
        
    return path.absolute()

# --- Setup Command ---
@app.command("setup")
def run_setup():
    """Interactive setup for jolly-flow."""
    console.print("[bold cyan]🎩 Welcome to jolly-flow Setup![/bold cyan]")
    
    # 1. Vault Root
    current_vault = ConfigManager.get_vault_root()
    vault_root = typer.prompt(
        "Enter the root directory for your private project vaults (where docs live)",
        default=current_vault
    )
    ConfigManager.set_key("vault_root", vault_root)
    
    # 2. Projects Root
    current_projects = ConfigManager.get_projects_root()
    projects_root = typer.prompt(
        "Enter the root directory for your public project repositories (where code lives)",
        default=current_projects
    )
    ConfigManager.set_key("projects_root", projects_root)
    
    console.print("\n[bold green]✅ Configuration saved![/bold green]")
    console.print(f"Vaults: [magenta]{vault_root}[/magenta]")
    console.print(f"Projects: [magenta]{projects_root}[/magenta]")

# --- Config Commands ---
@config_app.command("set-langsmith-key")
def set_langsmith_key(key: str = typer.Argument(..., help="LangSmith API Key")):
    """Sets the LangSmith API Key for observability."""
    ConfigManager.set_key("langsmith_api_key", key)
    console.print("[green]✅ LangSmith API Key saved.[/green]")

@config_app.command("set-workspace-id")
def set_workspace_id(workspace_id: str = typer.Argument(..., help="LangSmith Workspace ID")):
    """Sets the LangSmith Workspace ID (required for some org-scoped keys)."""
    ConfigManager.set_key("langsmith_workspace_id", workspace_id)
    console.print("[green]✅ LangSmith Workspace ID saved.[/green]")

@config_app.command("show")
def show_config():
    """Shows the current configuration."""
    key = ConfigManager.get_key("langsmith_api_key")
    ws_id = ConfigManager.get_key("langsmith_workspace_id")
    vault = ConfigManager.get_vault_root()
    projects = ConfigManager.get_projects_root()
    
    table = Table(title="jolly-flow Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Vault Root", vault)
    table.add_row("Projects Root", projects)
    
    if key:
        masked = key[:4] + "..." + key[-4:]
        table.add_row("LangSmith Key", masked)
    else:
        table.add_row("LangSmith Key", "[yellow]Not set[/yellow]")
        
    table.add_row("LangSmith Workspace", ws_id or "[yellow]Not set[/yellow]")
    
    console.print(table)


# --- Main Commands ---
@app.command()
def new_project(
    name: str = typer.Argument(..., help="Name of the project"),
    vault_root: str = typer.Option(None, help="Root directory for private vaults"),
    projects_root: str = typer.Option(None, help="Root directory for public repositories")
):
    """Scaffolds a new project."""
    v_root = vault_root or ConfigManager.get_vault_root()
    p_root = projects_root or ConfigManager.get_projects_root()
    create_project(name, v_root, p_root)

@app.command()
def sync(
    config: str = typer.Option(".jolly-sync.yaml", help="Path to the config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen without making changes")
):
    """Syncs docs from vault to repo."""
    sync_files(config, dry_run)

@app.command()
def generate_requirements(
    project: str = typer.Option(".", help="Project name or path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Interviews the user to define project scope and requirements."""
    project_path = str(resolve_project_path(project))
    if model is None:
        model = select_model_interactive("Requirements")
    run_agent_workflow(project_path, model, create_requirements_graph, "Requirements")

@app.command()
def generate_architecture(
    project: str = typer.Option(".", help="Project name or path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Designs the technical system architecture and stack."""
    project_path = str(resolve_project_path(project))
    if model is None:
        model = select_model_interactive("Architecture")
    run_agent_workflow(project_path, model, create_architecture_graph, "Architecture")

@app.command()
def generate_roadmap(
    project: str = typer.Option(".", help="Project name or path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Creates a phased implementation plan."""
    project_path = str(resolve_project_path(project))
    if model is None:
        model = select_model_interactive("Roadmap")
    run_agent_workflow(project_path, model, create_roadmap_graph, "Roadmap")

@app.command()
def start_phase(
    phase: str = typer.Argument(..., help="Phase number to start"),
    project: str = typer.Option(".", help="Project name or path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Generates detailed implementation guides for a specific phase."""
    project_path = str(resolve_project_path(project))
    if model is None:
        model = select_model_interactive(f"Phase {phase} Guide")
    run_agent_workflow(project_path, model, create_phase_guide_graph, f"Phase {phase} Guide", phase)

def run_agent_workflow(project_path: str, model: str, graph_factory, agent_name: str, phase: str = "0"):
    context_path = Path(project_path) / "AI-CONTEXT.md"
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found at {context_path}[/red]")
        console.print(f"[dim]Tip: Use 'cd' into your vault project folder or provide the project name via --project."[/dim])
        return

    with open(context_path, "r") as f:
        ai_context = f.read()

    console.print(f"[dim]📖 Loaded context from {context_path}[/dim]")

    initial_state = {
        "messages": [HumanMessage(content=f"Let's generate the {agent_name}.")],
        "project_name": "Unknown",
        "project_path": project_path,
        "templates_dir": "",
        "current_phase": phase,
        "instructions": "",
        "ai_context": ai_context
    }

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    graph = graph_factory(model)
    final_output = None
    
    for output in graph.stream(initial_state, config=config):
        for key, value in output.items():
            final_output = value
            if key == "agent":
                console.print(f"\n[bold green]🤖 Agent:[/bold green] {value['messages'][-1].content}")

    if final_output:
        print_token_usage(final_output)

@app.command()
def status(project: str = typer.Option(".", help="Project name or path to the project vault or repo")):
    """Shows current project status from AI-CONTEXT.md."""
    project_path = resolve_project_path(project)
    context_path = project_path / "AI-CONTEXT.md"
    
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found at {context_path}[/red]")
        return

    with open(context_path, "r") as f:
        content = f.read()

    phase_match = re.search(r"\*\*Current Phase:\*\* (.*)", content)
    status_match = re.search(r"- Status: (.*)", content)

    phase = phase_match.group(1) if phase_match else "Unknown"
    status = status_match.group(1) if status_match else "Unknown"

    table = Table(title=f"Status: {project_path.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Phase", phase)
    table.add_row("Status", status)
    table.add_row("Path", str(project_path))

    console.print(table)

if __name__ == "__main__":
    app()
