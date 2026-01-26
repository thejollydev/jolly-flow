import typer
import re
import os
import uuid
from pathlib import Path
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

# --- Defaults ---
DEFAULT_VAULT_ROOT = str(Path.home() / "Documents/jolly-vault")
DEFAULT_PROJECTS_ROOT = str(Path.home() / "Documents/jolly-projects")

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
    
    if key:
        masked = key[:4] + "..." + key[-4:]
        console.print(f"LangSmith API Key: [cyan]{masked}[/cyan]")
    else:
        console.print("LangSmith API Key: [yellow]Not set[/yellow]")
        
    if ws_id:
        console.print(f"LangSmith Workspace ID: [cyan]{ws_id}[/cyan]")
    else:
        console.print("LangSmith Workspace ID: [yellow]Not set[/yellow]")


# --- Main Commands ---
@app.command()
def new_project(
    name: str = typer.Argument(..., help="Name of the project"),
    vault_root: str = typer.Option(DEFAULT_VAULT_ROOT, help="Root directory for private vaults"),
    projects_root: str = typer.Option(DEFAULT_PROJECTS_ROOT, help="Root directory for public repositories")
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
    """Interviews the user to define project scope and requirements."""
    if model is None:
        model = select_model_interactive("Requirements")
    run_agent_workflow(project_path, model, create_requirements_graph, "Requirements")

@app.command()
def generate_architecture(
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Designs the technical system architecture and stack."""
    if model is None:
        model = select_model_interactive("Architecture")
    run_agent_workflow(project_path, model, create_architecture_graph, "Architecture")

@app.command()
def generate_roadmap(
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Creates a phased implementation plan."""
    if model is None:
        model = select_model_interactive("Roadmap")
    run_agent_workflow(project_path, model, create_roadmap_graph, "Roadmap")

@app.command()
def start_phase(
    phase: str = typer.Argument(..., help="Phase number to start"),
    project_path: str = typer.Option(".", help="Path to the project vault"),
    model: str = typer.Option(None, help="Model ID to use (interactive selection if not provided)")
):
    """Generates detailed implementation guides for a specific phase."""
    if model is None:
        model = select_model_interactive(f"Phase {phase} Guide")
    run_agent_workflow(project_path, model, create_phase_guide_graph, f"Phase {phase} Guide", phase)

def run_agent_workflow(project_path: str, model: str, graph_factory, agent_name: str, phase: str = "0"):
    context_path = Path(project_path) / "AI-CONTEXT.md"
    if not context_path.exists():
        console.print(f"[red]❌ Error: AI-CONTEXT.md not found in {project_path}[/red]")
        return

    with open(context_path, "r") as f:
        ai_context = f.read()

    console.print(f"[dim]📖 Loaded context from AI-CONTEXT.md[/dim]")

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
