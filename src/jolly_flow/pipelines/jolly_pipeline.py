"""
The Jolly Method - Open WebUI Pipe Function

This is a Pipe Function (not a Pipeline server) that wraps the jolly-flow CLI
and exposes it through Open WebUI's chat interface.
"""
import os
import asyncio
from typing import Union, AsyncGenerator
from pydantic import BaseModel, Field


class Pipe:
    """
    Open WebUI Pipe Function for The Jolly Method.

    Provides a chat interface to jolly-flow CLI commands.
    """

    class Valves(BaseModel):
        """Configuration settings for The Jolly Method pipe function."""
        jolly_path: str = Field(
            default="/home/joseph/GoogleDrive/Projects/the-jolly-method/jolly_flow/.venv/bin/jolly-flow",
            description="Path to the jolly-flow executable in the virtual environment"
        )
        pythonpath: str = Field(
            default="/home/joseph/GoogleDrive/Projects/the-jolly-method/jolly_flow/src",
            description="PYTHONPATH for jolly-flow execution"
        )

    def __init__(self):
        self.name = "The Jolly Method"
        self.valves = self.Valves()

    async def pipe(
        self,
        body: dict,
        __user__: dict = None,
        __request__: dict = None
    ) -> Union[str, AsyncGenerator[str, None]]:
        """
        Processes user messages and routes them to jolly-flow CLI commands.

        Args:
            body: Request body containing messages and model info
            __user__: User information (optional)
            __request__: Request object (optional)

        Returns:
            String response or async generator for streaming output
        """
        # Extract data from body
        messages = body.get("messages", [])
        if not messages:
            return "No messages received. Please send a command."

        user_message = messages[-1].get("content", "")
        model_id = body.get("model", "")

        # Validate command format
        if not user_message.startswith("/"):
            return (
                "**The Jolly Method** - Please use a command starting with `/`\n\n"
                "Available commands:\n"
                "- `/status` - Show current project status\n"
                "- `/sync` - Synchronize vault docs to repo\n"
                "- `/sync --dry-run` - Preview sync changes\n"
                "- `/generate requirements` - Start requirements gathering\n"
                "- `/generate architecture` - Start architecture design\n"
                "- `/generate roadmap` - Start roadmap planning\n"
                "- `/start-phase N` - Generate phase N guides\n"
            )

        # Parse command
        command = user_message[1:].strip().split()

        if not command:
            return "Empty command. Please specify a jolly-flow command."

        # Map chat commands to CLI commands
        # Example: /generate requirements -> jolly-flow generate-requirements
        if command[0] == "generate" and len(command) > 1:
            cli_cmd = [self.valves.jolly_path, f"generate-{command[1]}"]
        else:
            cli_cmd = [self.valves.jolly_path] + command

        try:
            # Execute jolly-flow command as subprocess
            process = await asyncio.create_subprocess_exec(
                *cli_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env={
                    **os.environ,
                    "PYTHONPATH": self.valves.pythonpath
                }
            )

            # Stream output line by line
            async def stream_output() -> AsyncGenerator[str, None]:
                """Stream subprocess output to chat interface."""
                while True:
                    line = await process.stdout.readline()
                    if line:
                        yield line.decode()
                    else:
                        break

                # Wait for process to complete
                await process.wait()

                # Report exit code if non-zero
                if process.returncode != 0:
                    yield f"\n⚠️ Command exited with code {process.returncode}\n"

            return stream_output()

        except FileNotFoundError:
            return (
                f"❌ Error: jolly-flow executable not found at:\n"
                f"`{self.valves.jolly_path}`\n\n"
                f"Please check the Valves configuration and ensure jolly-flow is installed."
            )
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"
