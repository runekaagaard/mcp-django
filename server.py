import os

from mcp.server.fastmcp import FastMCP

DJANGO_PATH = os.environ["DJANGO_PATH"]
PROJECT_PATH = os.environ["PROTECT_PATH"]

mcp = FastMCP("Djanco MCP")

@mcp.tool(description=f"Returns the output of `python manage.py` for the django project at {DJANGO_PATH}")
def list_management_commands() -> str:
    pass

@mcp.tool(description=
          f"Returns the output of `python manage.py [command_name] --help` for the django project at {DJANGO_PATH}"
         )
def help_management_command(command_name: str) -> str:
    pass

@mcp.tool(description=f"Run `python manage.py [command_name] [options]` for the django project at {DJANGO_PATH}")
def run_management_command(command_name: str, options=None) -> str:
    pass
