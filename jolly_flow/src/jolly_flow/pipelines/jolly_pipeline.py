import os
import asyncio
from typing import List, Union, Generator, Iterator

class Pipeline:
    def __init__(self):
        self.name = "The Jolly Method"
        # Path to the jolly-flow executable in the venv
        self.jolly_path = "/home/joseph/GoogleDrive/Projects/the-jolly-method/jolly_flow/venv/bin/jolly-flow"

    async def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        """
        Processes the user message and routes it to jolly-flow CLI.
        """
        if not user_message.startswith("/"):
            return "Please use a command starting with / (e.g., /status, /sync, /generate requirements)"

        command = user_message[1:].strip().split()
        
        # Mapping chat commands to CLI commands
        # Example: /generate requirements -> jolly-flow generate-requirements
        if command[0] == "generate" and len(command) > 1:
            cli_cmd = [self.jolly_path, f"generate-{command[1]}"]
        else:
            cli_cmd = [self.jolly_path] + command

        try:
            process = await asyncio.create_subprocess_exec(
                *cli_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env={**os.environ, "PYTHONPATH": "/home/joseph/GoogleDrive/Projects/the-jolly-method/jolly_flow/src"}
            )

            async def stream_output():
                while True:
                    line = await process.stdout.readline()
                    if line:
                        yield line.decode()
                    else:
                        break
                await process.wait()

            return stream_output()

        except Exception as e:
            return f"Error executing command: {str(e)}"
