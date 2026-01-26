#!/usr/bin/env python3
"""
Test script for The Jolly Method Pipe Function

This script tests the pipe function logic locally before installing in Open WebUI.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import jolly_pipeline
sys.path.insert(0, str(Path(__file__).parent))

from jolly_pipeline import Pipe


async def test_pipe_function():
    """Test the Pipe Function with various commands."""

    print("=" * 60)
    print("Testing The Jolly Method Pipe Function")
    print("=" * 60)
    print()

    # Initialize the pipe
    pipe = Pipe()
    print(f"✅ Pipe initialized: {pipe.name}")
    print(f"✅ jolly_path: {pipe.valves.jolly_path}")
    print(f"✅ pythonpath: {pipe.valves.pythonpath}")
    print()

    # Test 1: Help message (no slash command)
    print("-" * 60)
    print("Test 1: Help message (no slash command)")
    print("-" * 60)
    body = {
        "messages": [
            {"role": "user", "content": "hello"}
        ],
        "model": "the-jolly-method"
    }
    result = await pipe.pipe(body)
    print(result)
    print()

    # Test 2: Empty command
    print("-" * 60)
    print("Test 2: Empty command")
    print("-" * 60)
    body = {
        "messages": [
            {"role": "user", "content": "/"}
        ],
        "model": "the-jolly-method"
    }
    result = await pipe.pipe(body)
    print(result)
    print()

    # Test 3: /status command
    print("-" * 60)
    print("Test 3: /status command (streaming)")
    print("-" * 60)
    body = {
        "messages": [
            {"role": "user", "content": "/status"}
        ],
        "model": "the-jolly-method"
    }
    result = await pipe.pipe(body)

    # Check if it's a generator (streaming)
    if hasattr(result, '__anext__'):
        print("📡 Streaming output:")
        async for chunk in result:
            print(chunk, end='', flush=True)
        print()
    else:
        print(result)
    print()

    # Test 4: Invalid jolly-flow path
    print("-" * 60)
    print("Test 4: Invalid jolly-flow path (error handling)")
    print("-" * 60)
    pipe.valves.jolly_path = "/nonexistent/path/to/jolly-flow"
    body = {
        "messages": [
            {"role": "user", "content": "/status"}
        ],
        "model": "the-jolly-method"
    }
    result = await pipe.pipe(body)
    print(result)
    print()

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_pipe_function())
