import typer
from rich.console import Console
from .state import ProjectState

console = Console()

def human_review(state: ProjectState):
    console.print('\n[bold cyan]📋 Review Required[/bold cyan]')
    console.print('Please review the generated artifact.')
    
    choice = typer.prompt(
        'Do you want to [A]pprove, [R]evise, or [C]ancel?',
        default='A'
    ).upper()

    if choice == 'A':
        return {'messages': [{'role': 'user', 'content': 'APPROVED'}]}
    elif choice == 'R':
        feedback = typer.prompt('Enter your feedback for revision')
        return {'messages': [{'role': 'user', 'content': f'REVISE: {feedback}'}]}
    else:
        console.print('[red]Operation cancelled by user.[/red]')
        raise typer.Exit()
