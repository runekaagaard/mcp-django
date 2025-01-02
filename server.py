import os
import subprocess
from typing import Optional

from mcp.server.fastmcp import FastMCP

DJANGO_PATH = os.environ["DJANGO_PATH"]
PYTHON_PATH = os.environ["PYTHON_PATH"]
MAX_OUTPUT = int(os.environ.get("MAX_OUTPUT", 5000))

def execute_command(cmd: list[str]) -> str:
    """Execute a command and return its output, truncated if necessary."""
    try:
        result = subprocess.run(cmd, cwd=DJANGO_PATH, capture_output=True, text=True, check=True)
        output = result.stdout
        if len(output) > MAX_OUTPUT:
            output = output[:MAX_OUTPUT] + "[TRUNCATED]"
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

mcp = FastMCP("Django MCP")

@mcp.tool(description=f"Returns the output of `python manage.py` for the django project at {DJANGO_PATH}")
def list_management_commands() -> str:
    """List all available Django management commands."""
    return execute_command([PYTHON_PATH, "manage.py"])

@mcp.tool(description=
          f"Returns the output of `python manage.py help [command_name]` for the django project at {DJANGO_PATH}")
def help_management_command(command_name: str) -> str:
    """Get help for a specific Django management command."""
    return execute_command([PYTHON_PATH, "manage.py", command_name, "--help"])

@mcp.tool(description=f"Run `python manage.py [command_name] [options]` for the django project at {DJANGO_PATH}")
def run_management_command(command_name: str, options: Optional[list[str]] = None) -> str:
    """Run a Django management command with optional arguments."""
    cmd = [PYTHON_PATH, "manage.py", command_name]
    if options:
        cmd += options
    return execute_command(cmd)

if __name__ == "__main__":
    mcp.run()
