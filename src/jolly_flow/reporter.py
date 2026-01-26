from rich.console import Console
from rich.table import Table

console = Console()

def print_token_usage(final_state: dict):
    """Parses and prints token usage from the final state messages."""
    messages = final_state.get("messages", [])
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    
    # Iterate through messages to find token usage metadata
    # LangChain/ChatOpenAI puts this in response_metadata['token_usage']
    for msg in messages:
        if hasattr(msg, "response_metadata"):
            usage = msg.response_metadata.get("token_usage", {})
            total_tokens += usage.get("total_tokens", 0)
            prompt_tokens += usage.get("prompt_tokens", 0)
            completion_tokens += usage.get("completion_tokens", 0)
    
    if total_tokens > 0:
        table = Table(title="Token Usage", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Prompt Tokens", str(prompt_tokens))
        table.add_row("Completion Tokens", str(completion_tokens))
        table.add_row("Total Tokens", str(total_tokens))
        
        console.print(table)
        console.print("[dim]Note: Usage tracking depends on model provider support.[/dim]")
