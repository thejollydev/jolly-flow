import typer
from rich.console import Console
from .state import ProjectState

console = Console()

def human_review(state: ProjectState):
    """
    Interacts with the user to review the agent's output.
    Allows the user to Answer questions (Reply), Request changes (Revise), or Approve the result.
    """
    console.print('\n[bold cyan]🗣️  User Input Required[/bold cyan]')
    console.print('The agent has paused. You can:')
    console.print('  1. [bold green]Answer[/bold green] the agent\'s questions.')
    console.print('  2. [bold green]Revise[/bold green] the draft if it generated one.')
    console.print('  3. [bold green]Approve[/bold green] to save and exit (only if you are satisfied).')
    
    choice = typer.prompt(
        '\nAction? [r]eply/revise, [a]pprove, [c]ancel',
        default='r'
    ).lower()

    if choice.startswith('a'):
        return {'messages': [{'role': 'user', 'content': 'APPROVED'}]}
    
    elif choice.startswith('r'):
        user_input = typer.prompt('Your response')
        # We pass the input directly back to the agent.
        # The agent's history will show this as the user's turn.
        return {'messages': [{'role': 'user', 'content': user_input}]}
    
    else:
        console.print('[red]Operation cancelled by user.[/red]')
        raise typer.Exit()
