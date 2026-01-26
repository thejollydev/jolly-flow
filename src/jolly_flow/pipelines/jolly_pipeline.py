"""
jolly-flow - Open WebUI Pipe Function

Exposes jolly-flow CLI agents to the Open WebUI chat interface.
"""
import os
import asyncio
import sys
from typing import Union, AsyncGenerator
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        source_path: str = Field(
            default="/home/joseph/GoogleDrive/Projects/jolly-flow",
            description="Path to the jolly-flow source directory (must be mounted in Docker)"
        )

    def __init__(self):
        self.name = "jolly-flow"
        self.valves = self.Valves()
        self._installed = False

    async def ensure_installed(self):
        """Installs the package in the container environment if missing."""
        if self._installed: return
        
        try:
            test = await asyncio.create_subprocess_exec(
                "jolly-flow", "--version",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await test.wait()
            if test.returncode == 0:
                self._installed = True
                return
        except FileNotFoundError:
            pass

        yield "⚙️ Bootstrapping jolly-flow in container...\n"
        try:
            install = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "pip", "install", "-e", ".",
                cwd=self.valves.source_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            async for line in install.stdout:
                yield f"  > {line.decode()}"
            
            await install.wait()
            if install.returncode == 0:
                self._installed = True
                yield "✅ Bootstrap complete!\n\n"
            else:
                yield "❌ Bootstrap failed.\n"
        except Exception as e:
            yield f"❌ Error: {str(e)}\n"

    async def pipe(self, body: dict, __user__: dict = None) -> Union[str, AsyncGenerator[str, None]]:
        messages = body.get("messages", [])
        if not messages: return "No messages received."
        
        user_message = messages[-1].get("content", "").strip()
        if not user_message.startswith("/"):
            return (
                "**jolly-flow** - Please use a slash command:\n\n"
                "- `/status` - Current phase & status\n"
                "- `/sync` - Transform & sync docs\n"
                "- `/generate requirements` - Start interview\n"
                "- `/start-phase N` - Get guides"
            )

        args = user_message[1:].split()
        if not args: return "Empty command."

        if args[0] == "generate" and len(args) > 1:
            final_cmd = ["jolly-flow", f"generate-{args[1]}"] + args[2:]
        else:
            final_cmd = ["jolly-flow"] + args

        async def stream_output():
            async for log in self.ensure_installed():
                yield log
            
            if not self._installed:
                yield "Error: jolly-flow is not installed in the container."
                return

            try:
                process = await asyncio.create_subprocess_exec(
                    *final_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    env=os.environ
                )
                while True:
                    line = await process.stdout.readline()
                    if line: yield line.decode() 
                    else: break
                await process.wait()
            except Exception as e:
                yield f"❌ Execution Error: {str(e)}"

        return stream_output()
