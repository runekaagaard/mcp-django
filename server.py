import os
import subprocess
from typing import Optional

from mcp.server.fastmcp import FastMCP

DJANGO_PATH = os.environ["DJANGO_PATH"]
PYTHON_PATH = os.environ["PYTHON_PATH"]
MAX_OUTPUT = int(os.environ.get("MAX_OUTPUT", 5000))
LOG_PATH = os.environ.get("LOG_PATH")

# Create log file if it doesn't exist
if LOG_PATH:
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'w') as f:
                pass  # Just create the file
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")

def execute_command(cmd: list[str]) -> str:
    """Execute a command and return its output, truncated if necessary."""
    try:
        output_lines = []
        total_length = 0
        truncated = False
        
        # Add command and separator to output
        command_line = f"$ {' '.join(cmd)}"
        separator = '=' * len(command_line)
        command_str = f"\n{command_line}\n{separator}\n\n"
        output_lines.append(command_str)
        total_length += len(command_str)
        
        # Log command if logging enabled
        if LOG_PATH:
            with open(LOG_PATH, 'a') as log_file:
                log_file.write(command_str)
                log_file.flush()
        
        process = subprocess.Popen(
            cmd,
            cwd=DJANGO_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line:
                if LOG_PATH:
                    with open(LOG_PATH, 'a') as log_file:
                        log_file.write(line)
                        log_file.flush()
                
                if not truncated:
                    new_length = total_length + len(line)
                    if new_length <= MAX_OUTPUT:
                        output_lines.append(line)
                        total_length = new_length
                    else:
                        truncated = True
        
        return_code = process.wait()
        stderr = process.stderr.read()
        
        if return_code != 0:
            if LOG_PATH:
                with open(LOG_PATH, 'a') as log_file:
                    log_file.write(f"Error executing command: {stderr}\n")
            return f"Error executing command: {stderr}"
            
        output = ''.join(output_lines)
        if truncated:
            output += "[TRUNCATED]"
            
        return output
        
    except Exception as e:
        if LOG_PATH:
            with open(LOG_PATH, 'a') as log_file:
                log_file.write(f"Error executing command: {str(e)}\n")
        return f"Error executing command: {str(e)}"

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
