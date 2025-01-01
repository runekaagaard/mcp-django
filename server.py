import os
import subprocess
from typing import Optional

from mcp.server.fastmcp import FastMCP

DJANGO_PATH = os.environ["DJANGO_PATH"]
PROJECT_PATH = os.environ["PROTECT_PATH"]

mcp = FastMCP("Django MCP")

@mcp.tool(description=f"Returns the output of `python manage.py` for the django project at {DJANGO_PATH}")
def list_management_commands() -> str:
    """List all available Django management commands."""
    try:
        result = subprocess.run(
            ["python", "manage.py", "--help"],
            cwd=DJANGO_PATH,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error listing management commands: {e.stderr}"

@mcp.tool(description=
          f"Returns the output of `python manage.py [command_name] --help` for the django project at {DJANGO_PATH}"
         )
def help_management_command(command_name: str) -> str:
    """Get help for a specific Django management command."""
    try:
        result = subprocess.run(
            ["python", "manage.py", command_name, "--help"],
            cwd=DJANGO_PATH,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error getting help for command '{command_name}': {e.stderr}"

@mcp.tool(description=f"Run `python manage.py [command_name] [options]` for the django project at {DJANGO_PATH}")
def run_management_command(command_name: str, options: Optional[str] = None) -> str:
    """Run a Django management command with optional arguments."""
    cmd = ["python", "manage.py", command_name]
    
    if options:
        cmd.extend(options.split())
    
    try:
        result = subprocess.run(
            cmd,
            cwd=DJANGO_PATH,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running command '{command_name}': {e.stderr}"
