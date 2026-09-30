"""Interactive model selection with quota display"""
import typer
from rich.console import Console
from rich.table import Table
import requests

from jolly_flow import cliproxy

console = Console()


def get_available_models():
    """Get available models from CLIProxyAPI

    Returns:
        List of model dicts with id and name
    """
    try:
        response = requests.get(
            f"{cliproxy.base_url()}/models",
            headers={"Authorization": f"Bearer {cliproxy.api_key()}"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            console.print(f"[yellow]⚠️  Could not fetch models from CLIProxyAPI (status {response.status_code})[/yellow]")
            return []
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not connect to CLIProxyAPI: {e}[/yellow]")
        return []


def get_quota_info(model_id: str) -> dict:
    """Get quota information for a model (stubbed for now)

    Args:
        model_id: The model ID

    Returns:
        Dict with quota info (stubbed - future implementation)
    """
    # TODO: Implement actual quota tracking
    # For now, return stubbed data
    if "claude" in model_id.lower():
        return {"usage": "Unknown", "limit": "Subscription", "percent": "?"}
    elif "gemini" in model_id.lower():
        return {"usage": "Unknown", "limit": "Subscription", "percent": "?"}
    elif "ollama" in model_id.lower() or "qwen" in model_id.lower():
        return {"usage": "0", "limit": "Unlimited", "percent": "100"}
    else:
        return {"usage": "Unknown", "limit": "Unknown", "percent": "?"}


def select_model_interactive(agent_name: str = "Agent") -> str:
    """Interactively select a model with quota display

    Args:
        agent_name: Name of the agent (e.g., "Requirements", "Architecture")

    Returns:
        Selected model ID
    """
    console.print(f"\n[bold cyan]🤖 Select Model for {agent_name} Agent[/bold cyan]")

    # Get available models
    models = get_available_models()

    if not models:
        console.print("[yellow]⚠️  Using default model (CLIProxyAPI not available)[/yellow]")
        return "gemini-2.5-flash-lite"

    # Build table
    table = Table(title="Available Models")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Model", style="green")
    table.add_column("Quota", style="yellow")
    table.add_column("Status", style="magenta")

    for idx, model in enumerate(models, 1):
        model_id = model.get("id", "unknown")
        quota = get_quota_info(model_id)

        # Determine status
        if quota["limit"] == "Unlimited":
            status = "✅ Free/Local"
        else:
            status = f"📊 {quota['percent']}% available"

        table.add_row(
            str(idx),
            model_id,
            quota["limit"],
            status
        )

    console.print(table)

    # Prompt for selection
    while True:
        try:
            choice = typer.prompt(
                f"\nSelect model (1-{len(models)}) or press Enter for default",
                default="1"
            )

            choice_num = int(choice)
            if 1 <= choice_num <= len(models):
                selected = models[choice_num - 1]["id"]
                console.print(f"[green]✅ Selected: {selected}[/green]")
                return selected
            else:
                console.print(f"[red]Invalid choice. Please enter 1-{len(models)}[/red]")
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a number 1-{len(models)}[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Using default model[/yellow]")
            return models[0]["id"] if models else "gemini-2.5-flash-lite"
