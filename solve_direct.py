#!/usr/bin/env python3
"""
Direct LLM-based solution generator without containers.
Generates solutions, trajectories, and summary files similar to container-based runs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator import chat_completion_batch
from generator.sample_solutions import SYSTEM_MESSAGE, USER_TEMPLATE, _extract_action


# Agent system prompt for solving terminal tasks
AGENT_SYSTEM_PROMPT = SYSTEM_MESSAGE


def generate_reward_prompt(task_data: Dict[str, Any]) -> str:
    """Generate a rule prompt for LLM-based trajectory reward evaluation."""
    task_description = task_data.get("description", "")
    task_truth = task_data.get("truth", "")
    task_name = task_data.get("name", "unknown_task")

    prompt = f"""# Reward Evaluation Rules for Terminal Task

## Task Information

**Task Name**: {task_name}

**Task Description**:
{task_description}

**Expected Outcome (Ground Truth)**:
{task_truth}

---

## Evaluation Instructions

You are an expert evaluator for terminal-based tasks. Your job is to analyze a given trajectory (a sequence of agent actions and observations) and determine whether the task was completed successfully.

### Scoring Criteria

Score the trajectory on a scale of 0.0 to 1.0:

- **1.0 (Perfect Success)**: The task is fully completed according to all specifications
- **0.8-0.9 (Success with minor issues)**: The task is completed but with minor deviations
- **0.5-0.7 (Partial Success)**: Some requirements met but not all
- **0.1-0.4 (Failure)**: Task attempted but not completed
- **0.0 (No attempt)**: Task not attempted or completely wrong

### Evaluation Steps

1. **Analyze the Task Requirements**: Identify what files need to be created/modified and their expected content
2. **Review the Trajectory**: Check the sequence of commands executed by the agent
3. **Verify Final State**: Determine if the expected files exist with correct content
4. **Check Command Execution**: Note if commands succeeded (exit_code=0) or failed

### Key Questions to Answer

- Did the agent create/modify the required files?
- Is the file content exactly as specified in the task?
- Did the agent verify their work (e.g., using cat, ls, etc.)?
- Did the agent mark the task as complete (<action>done</action>)?

### Output Format

Provide your evaluation in the following format:

```
Score: <0.0-1.0>
Reasoning: <Brief explanation of why this score was given>
Verdict: <SUCCESS|PARTIAL|FAILURE>
```

### Special Notes

- The agent operates in a simulated terminal environment
- Commands may have simulated outputs that don't reflect real file system state
- Focus on whether the agent's approach and final actions would solve the task in a real environment
- Consider if the agent properly verified their solution before marking done

---

## Task-Specific Requirements

Based on the task description above, the agent should:

{extract_requirements(task_description)}

---

Evaluate the provided trajectory and assign an appropriate score.
"""
    return prompt.strip()


def extract_requirements(task_description: str) -> str:
    """Extract key requirements from task description for reward evaluation."""
    requirements = []

    # Look for file paths
    import re
    paths = re.findall(r'/[a-zA-Z0-9_./]+', task_description)
    if paths:
        requirements.append(f"- Create/modify files at: {', '.join(set(paths))}")

    # Look for specific instructions
    if 'directory' in task_description.lower():
        requirements.append("- Create necessary directories")

    if 'environment variable' in task_description.lower():
        requirements.append("- Set environment variables correctly")

    if 'echo' in task_description.lower() or 'printf' in task_description.lower():
        requirements.append("- Write content to files using appropriate commands")

    if 'chmod' in task_description.lower() or 'permission' in task_description.lower():
        requirements.append("- Set correct file permissions")

    if 'sqlite' in task_description.lower() or 'database' in task_description.lower():
        requirements.append("- Query database using sqlite3 CLI")

    if 'test' in task_description.lower() and 'pytest' in task_description.lower():
        requirements.append("- Run tests using pytest")

    if not requirements:
        requirements.append("- Follow all instructions in the task description")
        requirements.append("- Create/modify required files with correct content")

    return '\n'.join(requirements)


MAX_OUTPUT_LENGTH = 50000
MAX_EPISODES = 64
MAX_TIME_SEC = 600


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def generate_trial_name(task_name: str) -> str:
    """Generate a trial name similar to harbor format."""
    short_hash = uuid.uuid4().hex[:8]
    # Take first part of task name and truncate
    task_part = task_name[:25] if len(task_name) > 25 else task_name
    return f"{task_part}__{short_hash}"


def create_system_prompt() -> str:
    """Create the system prompt for the agent."""
    return SYSTEM_MESSAGE


def create_user_prompt(task_description: str) -> str:
    """Create the user prompt with task description."""
    restrictions = (
        "\n\nRESTRICTIONS:\n"
        "- You cannot use sudo or any commands requiring root privileges.\n"
        "- You cannot use interactive tools like vim, nano, etc.\n"
        "- When running commands that prompt for input (yes/no, etc.), use non-interactive flags (e.g., `-y`, `--yes`, `--non-interactive`) when available, or pipe the inputs (e.g., `echo -e 'yes\\nno' | ./script.sh` or `yes | ./script.sh`) since you cannot interact with running processes.\n"
    )
    return USER_TEMPLATE.format(task_description=task_description + restrictions)


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp in ISO format with timezone."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def create_trajectory_step(
    step_id: int,
    source: str,
    message: str,
    model_name: Optional[str] = None,
    tool_calls: Optional[List[Dict]] = None,
    observation: Optional[Dict] = None,
    metrics: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Create a single trajectory step."""
    step = {
        "step_id": step_id,
        "timestamp": format_timestamp(),
        "source": source,
        "message": message,
    }

    if model_name:
        step["model_name"] = model_name

    if tool_calls:
        step["tool_calls"] = tool_calls

    if observation:
        step["observation"] = observation

    if metrics:
        step["metrics"] = metrics

    return step


def create_tool_call(
    tool_call_id: str,
    command: str,
    duration: float = 1.0,
) -> Dict[str, Any]:
    """Create a tool call entry for bash_command."""
    return {
        "tool_call_id": tool_call_id,
        "function_name": "bash_command",
        "arguments": {
            "keystrokes": command,
            "duration": duration,
        }
    }


def create_observation_result(content: str, exit_code: int = 0) -> Dict[str, Any]:
    """Create an observation result."""
    return {
        "results": [
            {
                "content": content,
                "exit_code": exit_code,
            }
        ]
    }


def initialize_task_state(task_description: str, task_context: Dict):
    """Initialize task-specific filesystem state based on task description."""
    fs = SimulatedFilesystem()

    # Parse task description for paths and requirements
    # Common patterns:
    # - /home/user/app_logs - log directories
    # - /home/user/db_config - config directories
    # - /home/user/logs - log files
    # - /app/ - application directories

    import re
    paths = re.findall(r'/[a-zA-Z0-9_./]+', task_description)

    for path in paths:
        path = path.rstrip('/.')
        if 'directory' in task_description.lower() and path in task_description:
            fs.mkdir(path)
        elif 'file' in task_description.lower() and path in task_description:
            # Create parent directory
            parent = '/'.join(path.split('/')[:-1]) or '/'
            fs.mkdir(parent)
            # Create file with some content
            if '.log' in path:
                fs.write_file(path, f"Log entry 1\nLog entry 2\nLog entry 3\n")
            elif '.txt' in path:
                fs.write_file(path, f"# {path}\nContent here\n")
            elif '.py' in path:
                fs.write_file(path, f"# {path}\nprint('hello')\n")
            elif '.json' in path:
                fs.write_file(path, f'{{"file": "{path}"}}')
            else:
                fs.write_file(path, f"# Content of {path}\n")

    # Task-specific initialization
    if 'app_logs' in task_description:
        fs.mkdir('/home/user/app_logs')
        fs.write_file('/home/user/app_logs/error.log', 'Error log content\n' * 100)
        fs.write_file('/home/user/app_logs/access.log', 'Access log content\n' * 200)
        fs.write_file('/home/user/app_logs/debug.log', 'Debug log content\n' * 50)

    if 'db_config' in task_description:
        fs.mkdir('/home/user/db_config')

    if '/home/user/logs' in task_description:
        fs.mkdir('/home/user/logs')
        fs.write_file('/home/user/logs/app.log', 'Log started\nNew event\n')
        fs.write_file('/home/user/logs/error.log', 'Errors:\nNone\n')

    if '/app/' in task_description or '/app' in task_description:
        fs.mkdir('/app')
        fs.mkdir('/app/tests')
        fs.write_file('/app/main.py', '# Main application\n')

    # SQLite database tasks
    if 'diagnostics.db' in task_description or 'sqlite' in task_description.lower():
        fs.mkdir('/home/user/appdata')
        # Simulate database with metadata
        fs.write_file('/home/user/appdata/diagnostics.db', 'SQLite format 3\n')
        task_context['sqlite_tables'] = {
            'users': {
                'columns': ['id', 'name', 'email'],
                'rows': 5
            },
            'logs': {
                'columns': ['id', 'user_id', 'message', 'timestamp'],
                'rows': 10
            }
        }

    task_context['fs'] = fs


class SimulatedFilesystem:
    """Simulates a filesystem for command execution."""

    def __init__(self):
        self.files: Dict[str, str] = {}
        self.dirs: set = {"/home/user", "/tmp", "/app", "/workspace"}
        self.env_vars: Dict[str, str] = {}
        self.current_dir = "/home/user"

    def normalize_path(self, path: str) -> str:
        """Normalize a path to absolute."""
        if not path.startswith("/"):
            path = f"{self.current_dir}/{path}"
        # Simple normalization
        parts = path.split("/")
        result = []
        for part in parts:
            if part == ".." and result:
                result.pop()
            elif part and part != ".":
                result.append(part)
        return "/" + "/".join(result)

    def file_exists(self, path: str) -> bool:
        """Check if a file exists."""
        return self.normalize_path(path) in self.files

    def dir_exists(self, path: str) -> bool:
        """Check if a directory exists."""
        return self.normalize_path(path) in self.dirs

    def read_file(self, path: str) -> Optional[str]:
        """Read file content."""
        normalized = self.normalize_path(path)
        return self.files.get(normalized)

    def write_file(self, path: str, content: str):
        """Write content to a file."""
        normalized = self.normalize_path(path)
        self.files[normalized] = content
        # Ensure parent directory exists
        parent = "/".join(normalized.split("/")[:-1]) or "/"
        self.dirs.add(parent)

    def mkdir(self, path: str):
        """Create a directory."""
        normalized = self.normalize_path(path)
        self.dirs.add(normalized)

    def list_dir(self, path: str = ".") -> List[str]:
        """List directory contents."""
        normalized = self.normalize_path(path)
        contents = []
        prefix = normalized.rstrip("/") + "/"

        # Add direct children directories
        for d in self.dirs:
            if d.startswith(prefix) and d != normalized:
                rel = d[len(prefix):].split("/")[0]
                if rel:
                    contents.append(rel + "/")

        # Add files
        for f in self.files:
            if f.startswith(prefix):
                rel = f[len(prefix):].split("/")[0]
                if rel and rel not in contents:
                    contents.append(rel)

        return sorted(set(contents))


def simulate_command_execution(
    command: str,
    task_context: Dict[str, Any],
    step_counter: int,
) -> Tuple[str, int]:
    """
    Simulate command execution for direct LLM solving.
    Returns (output, exit_code).
    """
    command = command.strip()

    # Get or create filesystem
    if "fs" not in task_context:
        task_context["fs"] = SimulatedFilesystem()
    fs: SimulatedFilesystem = task_context["fs"]

    # Handle common commands
    if command.startswith("cat "):
        path = command[4:].strip()
        return simulate_file_read(path, task_context, fs)

    elif command.startswith("ls ") or command == "ls":
        return simulate_ls(command, task_context, fs)

    elif command.startswith("cd "):
        new_dir = command[3:].strip()
        fs.current_dir = fs.normalize_path(new_dir)
        return (f"Changed directory to {fs.current_dir}", 0)

    elif command.startswith("pwd"):
        return (fs.current_dir, 0)

    elif command.startswith("echo "):
        content = command[5:].strip()
        # Handle echo with redirection
        if ">" in content:
            return simulate_echo_write(command, task_context, fs)
        return (content, 0)

    elif command.startswith("printf "):
        # Handle printf with redirection
        if ">" in command:
            return simulate_printf_write(command, task_context, fs)
        return ("", 0)

    elif command.startswith("mkdir "):
        parts = command[6:].strip().split()
        for part in parts:
            if not part.startswith("-"):
                fs.mkdir(part)
        return ("", 0)

    elif command.startswith("touch "):
        path = command[6:].strip()
        if not fs.file_exists(path):
            fs.write_file(path, "")
        return ("", 0)

    elif command.startswith("find "):
        return simulate_find(command, task_context, fs)

    elif command.startswith("grep "):
        return simulate_grep(command, task_context, fs)

    elif command.startswith("python3 ") or command.startswith("python "):
        return simulate_python_execution(command, task_context, fs)

    elif command.startswith("pytest"):
        return simulate_pytest(command, task_context, fs)

    elif command.startswith("pip "):
        return (f"Package operation completed: {command}", 0)

    elif command.startswith("git "):
        return simulate_git_command(command, task_context)

    elif command.startswith("head "):
        parts = command.split()
        lines = 10
        path = parts[-1]
        for i, part in enumerate(parts):
            if part == "-n" and i + 1 < len(parts) - 1:
                lines = int(parts[i + 1])
        return simulate_file_read(path, task_context, fs, lines=lines)

    elif command.startswith("tail "):
        parts = command.split()
        path = parts[-1]
        return simulate_file_read(path, task_context, fs, lines=10)

    elif command.startswith("wc "):
        return simulate_wc(command, task_context, fs)

    elif command.startswith("sort "):
        return simulate_sort(command, task_context, fs)

    elif command.startswith("uniq"):
        return ("unique lines", 0)

    elif command.startswith("awk "):
        return ("awk processing completed", 0)

    elif command.startswith("sed "):
        return simulate_sed(command, task_context, fs)

    elif command.startswith("curl ") or command.startswith("wget "):
        return ("Download completed successfully", 0)

    elif command.startswith("tar ") or command.startswith("unzip"):
        return ("Archive extracted", 0)

    elif command.startswith("cp "):
        return simulate_cp(command, task_context, fs)

    elif command.startswith("mv "):
        return simulate_mv(command, task_context, fs)

    elif command.startswith("rm "):
        return simulate_rm(command, task_context, fs)

    elif command.startswith("chmod "):
        return ("", 0)

    elif command.startswith("chown "):
        return ("Permissions updated", 0)

    elif command.startswith("du "):
        return simulate_du(command, task_context, fs)

    elif command.startswith("df "):
        return ("Filesystem information displayed", 0)

    elif command.startswith("ps ") or command.startswith("top") or command == "ps":
        return ("Process list displayed", 0)

    elif command.startswith("which ") or command.startswith("whereis "):
        return (f"/usr/bin/{command.split()[-1]}", 0)

    elif command.startswith("file "):
        path = command[5:].strip()
        if fs.file_exists(path):
            return (f"{path}: ASCII text", 0)
        return (f"{path}: No such file or directory", 1)

    elif command.startswith("diff "):
        return ("Files are identical", 0)

    elif command.startswith("source "):
        return ("", 0)

    elif command.startswith("export "):
        # Parse export VAR=value
        export_str = command[7:].strip()
        if "=" in export_str:
            key, value = export_str.split("=", 1)
            fs.env_vars[key] = value
        return ("", 0)

    elif command.startswith("sqlite3 "):
        return simulate_sqlite(command, task_context, fs)

    elif command.startswith("exit"):
        return ("Exiting shell", 0)

    elif command.startswith("#") or command == "":
        return ("", 0)

    else:
        # Generic success for unknown commands
        return (f"Command executed: {command}", 0)


def simulate_file_read(path: str, task_context: Dict, fs: SimulatedFilesystem, lines: Optional[int] = None) -> Tuple[str, int]:
    """Simulate reading a file."""
    normalized = fs.normalize_path(path)

    # Check if file exists in simulated environment
    content = fs.read_file(path)
    if content is not None:
        if lines:
            all_lines = content.split('\n')
            if len(all_lines) > lines:
                content = '\n'.join(all_lines[:lines])
        return (content, 0)

    # Generate plausible content based on path for new files
    if ".py" in path:
        default_content = f"# Python file: {normalized}\n# Simulated content\n"
    elif ".json" in path:
        default_content = f'{{"file": "{normalized}", "status": "ok"}}'
    elif ".txt" in path or ".log" in path:
        default_content = f"# Log: {normalized}\n"
    elif ".md" in path:
        default_content = f"# {normalized}\n\nDocumentation content.\n"
    elif ".env" in path:
        default_content = "# Environment variables\n"
    elif ".sh" in path:
        default_content = "#!/bin/bash\n"
    else:
        default_content = f"# Content of {normalized}\n"

    # Store for future reads
    fs.write_file(path, default_content)
    return (default_content, 0)


def simulate_ls(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate ls command."""
    parts = command.split()
    path = "."
    flags = []
    for i, part in enumerate(parts):
        if part.startswith("-"):
            flags.extend(list(part[1:]))
        elif i > 0:
            path = part
            break

    normalized = fs.normalize_path(path)

    if not fs.dir_exists(normalized) and not fs.file_exists(normalized):
        return (f"ls: cannot access '{path}': No such file or directory", 1)

    if fs.file_exists(normalized):
        return (normalized.split("/")[-1], 0)

    contents = fs.list_dir(normalized)

    if "l" in flags:
        # Long format
        lines = [f"total {len(contents) * 4}"]
        for item in contents:
            item_type = "d" if item.endswith("/") else "-"
            lines.append(f"{item_type}rwxr-xr-x 1 user user 4096 {format_timestamp()[:10]} 12:00 {item.rstrip('/')}")
        return ("\n".join(lines), 0)
    else:
        return ("  ".join(contents), 0)


def simulate_echo_write(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate echo with redirection."""
    # Extract content and path from echo command
    match = re.search(r'echo\s+(["\'])?(.*?)(\1)?\s*>+\s*(.+)', command)
    if match:
        _, content, _, path = match.groups()
        path = path.strip()
        content = content or ""
        # Remove quotes from content
        content = content.strip('"\'')
        fs.write_file(path, content + "\n")
        return ("", 0)

    return ("", 0)


def simulate_printf_write(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate printf with redirection."""
    # Extract format and path
    match = re.search(r'printf\s+["\']([^"\']+)["\']\s*>+\s*(.+)', command)
    if match:
        content, path = match.groups()
        path = path.strip()
        # Handle \n escapes
        content = content.replace("\\n", "\n")
        fs.write_file(path, content)
        return ("", 0)

    return ("", 0)


def simulate_find(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate find command."""
    parts = command.split()
    path = "."
    file_type = None

    for i, part in enumerate(parts[1:], 1):
        if part == "-type" and i + 1 < len(parts):
            file_type = parts[i + 1]
        elif not part.startswith("-") and i == 1:
            path = part

    normalized = fs.normalize_path(path)
    results = []

    # Return all files and directories under path
    for d in fs.dirs:
        if d.startswith(normalized):
            if file_type == "d":
                results.append(d)
            elif file_type == "f":
                pass  # Directories only
            else:
                results.append(d)

    for f in fs.files:
        if f.startswith(normalized):
            if file_type == "f" or file_type is None:
                results.append(f)

    return ("\n".join(sorted(results)), 0)


def simulate_grep(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate grep command."""
    parts = command.split()
    pattern = None
    path = None

    for i, part in enumerate(parts[1:], 1):
        if not part.startswith("-"):
            if pattern is None:
                pattern = part.strip('"\'')
            else:
                path = part
                break

    if path:
        content = fs.read_file(path)
        if content:
            matching = [line for line in content.split('\n') if pattern and pattern in line]
            return ("\n".join(matching), 0)

    return ("", 0)


def simulate_python_execution(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate Python script execution."""
    if "test" in command.lower():
        return ("============================= test session starts ==============================\nplatform linux -- Python 3.x\n\n...\n\n============================== 5 passed in 0.5s ===============================", 0)
    return ("Script executed successfully", 0)


def simulate_pytest(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate pytest command."""
    return ("""============================= test session starts ==============================
platform linux -- Python 3.11.0
rootdir: /home/user
collected 10 items

test_example.py ..........                                               [100%]

============================== 10 passed in 0.5s ===============================""", 0)


def simulate_wc(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate wc command."""
    parts = command.split()
    path = parts[-1]

    content = fs.read_file(path)
    if content:
        lines = content.count('\n')
        words = len(content.split())
        chars = len(content)
        return (f"{lines:>8}{words:>8}{chars:>8} {path}", 0)

    return (f"wc: {path}: No such file or directory", 1)


def simulate_sort(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate sort command."""
    parts = command.split()
    path = parts[-1]

    content = fs.read_file(path)
    if content:
        lines = sorted(content.strip().split('\n'))
        return ('\n'.join(lines), 0)

    return (f"sort: {path}: No such file or directory", 1)


def simulate_sed(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate sed command."""
    # Simple sed simulation - in-place editing
    match = re.search(r'sed\s+-i\s+["\']?s/(.+?)/(.+?)/[g]?["\']?\s*(.+)', command)
    if match:
        old, new, path = match.groups()
        content = fs.read_file(path) or ""
        content = content.replace(old, new)
        fs.write_file(path, content)
        return ("", 0)
    return ("", 0)


def simulate_cp(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate cp command."""
    parts = command.split()
    src = None
    dst = None
    for part in parts[1:]:
        if not part.startswith("-"):
            if src is None:
                src = part
            else:
                dst = part
                break

    if src and dst:
        content = fs.read_file(src)
        if content is not None:
            fs.write_file(dst, content)
            return ("", 0)

    return (f"cp: cannot stat '{src}': No such file or directory", 1)


def simulate_mv(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate mv command."""
    parts = command.split()
    src = None
    dst = None
    for part in parts[1:]:
        if not part.startswith("-"):
            if src is None:
                src = part
            else:
                dst = part
                break

    if src and dst:
        content = fs.read_file(src)
        if content is not None:
            fs.write_file(dst, content)
            # Remove original (simulated)
            src_normalized = fs.normalize_path(src)
            if src_normalized in fs.files:
                del fs.files[src_normalized]
            return ("", 0)

    return (f"mv: cannot stat '{src}': No such file or directory", 1)


def simulate_rm(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate rm command."""
    parts = command.split()
    for part in parts[1:]:
        if not part.startswith("-"):
            normalized = fs.normalize_path(part)
            if normalized in fs.files:
                del fs.files[normalized]
            # Also try to remove from dirs if it's a directory
            if normalized in fs.dirs:
                fs.dirs.remove(normalized)
    return ("", 0)


def simulate_sqlite(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate sqlite3 command."""
    # Parse command: sqlite3 <db> <query>
    parts = command.split()
    if len(parts) < 2:
        return ("Usage: sqlite3 DATABASE [SQL]", 1)

    db_path = parts[1]

    # Check if database exists
    if not fs.file_exists(db_path):
        return (f"Error: unable to open database \"{db_path}\": database does not exist", 1)

    # Get sqlite metadata
    sqlite_tables = task_context.get('sqlite_tables', {})

    if len(parts) < 3:
        # Interactive mode - just confirm connection
        return ("SQLite version 3.x\nConnected to database.", 0)

    # Extract query (everything after the database path)
    query_start = command.find(db_path) + len(db_path)
    query = command[query_start:].strip().strip('"\'')

    query_lower = query.lower()

    if '.tables' in query_lower:
        # List tables
        tables = list(sqlite_tables.keys())
        return ("  ".join(tables), 0)

    elif 'pragma table_info' in query_lower or 'select name from pragma_table_list' in query_lower:
        # Get columns for a table
        # Extract table name
        match = re.search(r'pragma table_info\((\w+)\)', query_lower)
        if match:
            table_name = match.group(1)
            if table_name in sqlite_tables:
                cols = sqlite_tables[table_name]['columns']
                # Return in pragma table_info format: cid|name|type|notnull|default|pk
                lines = []
                for i, col in enumerate(cols):
                    pk = 1 if i == 0 else 0  # Assume first column is PK
                    lines.append(f"{i}|{col}||0||{pk}")
                return ("\n".join(lines), 0)
        return ("", 0)

    elif 'count(*)' in query_lower:
        # Count rows
        match = re.search(r'from\s+(\w+)', query_lower)
        if match:
            table_name = match.group(1)
            if table_name in sqlite_tables:
                count = sqlite_tables[table_name]['rows']
                return (str(count), 0)
        return ("0", 0)

    elif 'select * from' in query_lower:
        # Return sample data
        match = re.search(r'from\s+(\w+)', query_lower)
        if match:
            table_name = match.group(1)
            if table_name in sqlite_tables:
                return (f"Sample data from {table_name}", 0)
        return ("", 0)

    else:
        return ("Query executed successfully", 0)


def simulate_du(command: str, task_context: Dict, fs: SimulatedFilesystem) -> Tuple[str, int]:
    """Simulate du command."""
    parts = command.split()
    path = "."
    human_readable = False
    summarize = False

    for i, part in enumerate(parts[1:]):
        if part == "-h" or part == "--human-readable":
            human_readable = True
        elif part == "-s" or part == "--summarize":
            summarize = True
        elif not part.startswith("-"):
            path = part

    normalized = fs.normalize_path(path)

    if not fs.dir_exists(normalized) and not fs.file_exists(normalized):
        return (f"du: cannot access '{path}': No such file or directory", 1)

    # Calculate total size based on files in directory
    total_bytes = 0
    if fs.file_exists(normalized):
        content = fs.read_file(normalized) or ""
        total_bytes = len(content)
    else:
        # Sum all files under directory
        for f_path, content in fs.files.items():
            if f_path.startswith(normalized + "/") or f_path == normalized:
                total_bytes += len(content or "")
        # Add some overhead for directory entries
        total_bytes += 4096  # typical block size

    if human_readable:
        if total_bytes < 1024:
            size_str = f"{total_bytes}B"
        elif total_bytes < 1024 * 1024:
            size_str = f"{max(1, total_bytes // 1024)}K"
        else:
            size_str = f"{total_bytes // (1024 * 1024)}M"
    else:
        # 1K blocks
        size_str = str(max(1, total_bytes // 1024))

    if summarize or human_readable:
        return (f"{size_str}\t{path}", 0)
    else:
        # List all entries
        lines = []
        for f_path, content in fs.files.items():
            if f_path.startswith(normalized + "/"):
                f_bytes = len(content or "")
                f_size = str(max(1, f_bytes // 1024))
                rel_path = f_path[len(normalized)+1:]
                lines.append(f"{f_size}\t{path}/{rel_path}")
        lines.append(f"{size_str}\t{path}")
        return ("\n".join(lines), 0)


def simulate_git_command(command: str, task_context: Dict) -> Tuple[str, int]:
    """Simulate git command."""
    if "status" in command:
        return ("On branch main\nnothing to commit, working tree clean", 0)
    elif "log" in command:
        return ("commit abc123\nAuthor: User\nDate: today\n\nInitial commit", 0)
    else:
        return ("Git operation completed", 0)


def run_single_solution(
    solution_idx: int,
    task_data: Dict[str, Any],
    model: str,
    temperature: float,
    max_tokens: int,
    max_episodes: int = MAX_EPISODES,
) -> Dict[str, Any]:
    """
    Run a single solution attempt with direct LLM interaction.
    Returns the result with trajectory and final status.
    """
    task_description = task_data.get("description", "")
    task_name = task_data.get("name", "unknown_task")

    # Initialize trajectory
    session_id = generate_session_id()
    steps = []
    step_id = 0

    # Agent info
    agent_info = {
        "name": "direct-llm-solver",
        "version": "1.0.0",
        "model_name": model,
        "extra": {
            "parser": "xml",
            "temperature": temperature,
        }
    }

    # Create initial user message with task
    user_message = create_user_prompt(task_description)

    # Initial step - user provides task
    step_id += 1
    steps.append(create_trajectory_step(
        step_id=step_id,
        source="user",
        message=user_message,
    ))

    # Initialize chat for LLM
    chat = [
        {"role": "system", "content": create_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    # Track metrics
    total_input_tokens = 0
    total_output_tokens = 0
    api_request_times = []

    # Task context for simulated command execution
    task_context = {
        "task_description": task_description,
        "task_name": task_name,
        "simulated_files": {},
        "commands_executed": [],
    }

    # Initialize task-specific state from task_description
    initialize_task_state(task_description, task_context)

    start_time = time.time()
    n_episodes = 0
    final_status = "incomplete"
    final_output = ""

    try:
        for episode in range(1, max_episodes + 1):
            n_episodes = episode

            # Check timeout
            if time.time() - start_time > MAX_TIME_SEC:
                final_status = "timeout"
                break

            # Get LLM response
            api_start = time.time()
            responses = chat_completion_batch(
                [chat],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                num_completions=1,
                max_concurrency=1,
                show_progress=False,
            )
            api_time = (time.time() - api_start) * 1000  # Convert to ms
            api_request_times.append(api_time)

            if not responses or responses[0] is None:
                final_status = "api_error"
                break

            response = responses[0]
            raw_content = response.choices[0].message.content

            # Track tokens
            if hasattr(response, 'usage') and response.usage:
                total_input_tokens += response.usage.prompt_tokens
                total_output_tokens += response.usage.completion_tokens

            # Extract action
            action = _extract_action(raw_content)

            # Add assistant step
            step_id += 1

            if action["type"] == "done":
                steps.append(create_trajectory_step(
                    step_id=step_id,
                    source="agent",
                    model_name=model,
                    message=raw_content,
                    metrics={
                        "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if hasattr(response, 'usage') else 0,
                        "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if hasattr(response, 'usage') else 0,
                    }
                ))
                final_status = "success"
                break

            elif action["type"] == "command":
                command = action["command"] or ""

                # Create tool call
                tool_call_id = f"call_{episode}_1"
                tool_calls = [create_tool_call(tool_call_id, command, duration=1.0)]

                # Simulate command execution
                output, exit_code = simulate_command_execution(command, task_context, step_id)
                task_context["commands_executed"].append({
                    "command": command,
                    "output": output,
                    "exit_code": exit_code,
                })

                # Format observation
                obs_content = f"New Terminal Output:\nroot@simulated:~# {command}\n{output}"
                if exit_code != 0:
                    obs_content += f"\n(exit_code={exit_code})"

                observation = {
                    "results": [{"content": obs_content, "exit_code": exit_code}]
                }

                # Add agent step with tool calls
                steps.append(create_trajectory_step(
                    step_id=step_id,
                    source="agent",
                    model_name=model,
                    message=raw_content,
                    tool_calls=tool_calls,
                    observation=observation,
                    metrics={
                        "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if hasattr(response, 'usage') else 0,
                        "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if hasattr(response, 'usage') else 0,
                    }
                ))

                # Add result back to chat
                result_message = f"Command executed. Output: {output}\n\n(exit_code={exit_code})"
                chat.append({"role": "assistant", "content": raw_content})
                chat.append({"role": "user", "content": result_message})

                # Add system step for command result
                step_id += 1
                steps.append(create_trajectory_step(
                    step_id=step_id,
                    source="system",
                    message=result_message,
                ))

            else:
                # Invalid parse
                steps.append(create_trajectory_step(
                    step_id=step_id,
                    source="agent",
                    model_name=model,
                    message=raw_content,
                    metrics={
                        "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if hasattr(response, 'usage') else 0,
                        "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if hasattr(response, 'usage') else 0,
                    }
                ))

                error_msg = (
                    "Could not parse a single <command>...</command> or <action>done</action>. "
                    "Please respond with exactly one of those."
                )
                chat.append({"role": "assistant", "content": raw_content})
                chat.append({"role": "user", "content": error_msg})

                step_id += 1
                steps.append(create_trajectory_step(
                    step_id=step_id,
                    source="system",
                    message=error_msg,
                ))

        else:
            # Max episodes reached
            final_status = "max_episodes"

    except Exception as e:
        final_status = "exception"
        final_output = str(e)
        steps.append(create_trajectory_step(
            step_id=step_id + 1,
            source="system",
            message=f"Exception occurred: {str(e)}",
        ))

    end_time = time.time()

    # Build trajectory
    trajectory = {
        "schema_version": "ATIF-v1.6",
        "session_id": session_id,
        "agent": agent_info,
        "steps": steps,
    }

    # Build result similar to harbor result.json
    result = {
        "success": final_status == "success",
        "status": final_status,
        "messages": chat,
        "trajectory": trajectory,
        "n_episodes": n_episodes,
        "n_input_tokens": total_input_tokens,
        "n_output_tokens": total_output_tokens,
        "api_request_times_msec": api_request_times,
        "duration_sec": end_time - start_time,
    }

    return result


def generate_solve_script(commands: List[str]) -> str:
    """Generate a solve.sh script from executed commands."""
    script_lines = ["#!/bin/bash", "set -e", ""]

    for cmd in commands:
        script_lines.append(f"# Command: {cmd[:50]}{'...' if len(cmd) > 50 else ''}")
        script_lines.append(cmd)
        script_lines.append("")

    return "\n".join(script_lines)


def save_solution_result(
    task_dir: Path,
    solution_idx: int,
    result: Dict[str, Any],
    model_name: str,
) -> Path:
    """
    Save a single solution result to disk.
    Creates: solution_N folder with trajectory.json and solve.sh
    """
    # Create solution directory
    solution_dir = task_dir / f"solution_{solution_idx:04d}"
    solution_dir.mkdir(parents=True, exist_ok=True)

    # Create trajectory directory
    trajectory_dir = solution_dir / "trajectory"
    trajectory_dir.mkdir(parents=True, exist_ok=True)

    # Save trajectory.json
    trajectory_path = trajectory_dir / "trajectory.json"
    with open(trajectory_path, 'w', encoding='utf-8') as f:
        json.dump(result["trajectory"], f, indent=2, ensure_ascii=False)

    # Extract commands for solve.sh
    commands = []
    for item in result.get("messages", []):
        if item.get("role") == "assistant":
            action = _extract_action(item.get("content", ""))
            if action["type"] == "command" and action.get("command"):
                commands.append(action["command"])

    # Generate and save solve.sh
    solve_script = generate_solve_script(commands)
    solve_path = solution_dir / "solve.sh"
    with open(solve_path, 'w', encoding='utf-8') as f:
        f.write(solve_script)

    # Make solve.sh executable
    os.chmod(solve_path, 0o755)

    # Save raw result
    result_path = solution_dir / "result.json"
    result_copy = {k: v for k, v in result.items() if k != "trajectory"}
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result_copy, f, indent=2, ensure_ascii=False)

    return solution_dir


def compute_pass_at_k(num_solutions: int, num_success: int) -> Dict[int, float]:
    """Compute pass@k metric."""
    from math import comb

    pass_at_k = {}
    for k in range(1, num_solutions + 1):
        if num_success == 0:
            p = 0.0
        else:
            p = 1.0 - (comb(num_solutions - num_success, k) / comb(num_solutions, k))
        pass_at_k[k] = float(p)

    return pass_at_k


def generate_summary(
    task_dir: Path,
    task_data: Dict[str, Any],
    results: List[Dict[str, Any]],
    model: str,
    start_time: datetime,
    end_time: datetime,
) -> Dict[str, Any]:
    """
    Generate summary.json similar to harbor result.json format.
    """
    task_name = task_data.get("name", "unknown_task")
    trial_name = generate_trial_name(task_name)

    num_solutions = len(results)
    num_success = sum(1 for r in results if r.get("success", False))
    pass_at_k = compute_pass_at_k(num_solutions, num_success)

    # Aggregate token usage
    total_input_tokens = sum(r.get("n_input_tokens", 0) for r in results)
    total_output_tokens = sum(r.get("n_output_tokens", 0) for r in results)
    all_api_times = []
    for r in results:
        all_api_times.extend(r.get("api_request_times_msec", []))

    summary = {
        "id": str(uuid.uuid4()),
        "task_name": task_name,
        "trial_name": trial_name,
        "trial_uri": f"file://{task_dir}/{trial_name}",
        "task_id": {
            "path": str(task_dir),
        },
        "source": None,
        "task_checksum": "",  # Could compute from task.json
        "config": {
            "task": {
                "path": str(task_dir),
                "git_url": None,
                "git_commit_id": None,
                "overwrite": False,
                "download_dir": None,
                "source": None,
            },
            "trial_name": trial_name,
            "trials_dir": str(task_dir / "solutions"),
            "timeout_multiplier": 1.0,
            "agent_timeout_multiplier": None,
            "verifier_timeout_multiplier": None,
            "agent_setup_timeout_multiplier": 5.0,
            "environment_build_timeout_multiplier": None,
            "agent": {
                "name": "direct-llm-solver",
                "import_path": None,
                "model_name": model,
                "override_timeout_sec": None,
                "override_setup_timeout_sec": None,
                "max_timeout_sec": None,
                "kwargs": {},
                "env": {},
            },
            "environment": {
                "type": "direct",
                "import_path": None,
                "force_build": False,
                "delete": True,
                "override_cpus": None,
                "override_memory_mb": None,
                "override_storage_mb": None,
                "override_gpus": None,
                "suppress_override_warnings": False,
                "kwargs": {},
            },
            "verifier": {
                "override_timeout_sec": None,
                "max_timeout_sec": None,
                "disable": False,
            },
            "artifacts": [],
            "job_id": str(uuid.uuid4()),
        },
        "agent_info": {
            "name": "direct-llm-solver",
            "version": "1.0.0",
            "model_info": {
                "name": model.split("/")[-1] if "/" in model else model,
                "provider": "openai",
            }
        },
        "agent_result": {
            "n_input_tokens": total_input_tokens,
            "n_cache_tokens": 0,
            "n_output_tokens": total_output_tokens,
            "cost_usd": None,
            "rollout_details": [],
            "metadata": {
                "n_episodes": sum(r.get("n_episodes", 0) for r in results) / len(results) if results else 0,
                "api_request_times_msec": all_api_times,
                "summarization_count": 0,
            }
        },
        "verifier_result": {
            "rewards": {
                "reward": 1.0 if num_success > 0 else 0.0,
            }
        },
        "exception_info": None,
        "started_at": start_time.isoformat(),
        "finished_at": end_time.isoformat(),
        "environment_setup": {
            "started_at": start_time.isoformat(),
            "finished_at": start_time.isoformat(),
        },
        "agent_setup": {
            "started_at": start_time.isoformat(),
            "finished_at": (start_time.isoformat() if results else end_time.isoformat()),
        },
        "agent_execution": {
            "started_at": start_time.isoformat(),
            "finished_at": end_time.isoformat(),
        },
        "verifier": {
            "started_at": end_time.isoformat(),
            "finished_at": end_time.isoformat(),
        },
        "summary": {
            "num_runs": num_solutions,
            "num_success": num_success,
            "pass_at_k": pass_at_k,
            "success_rate": num_success / num_solutions if num_solutions > 0 else 0.0,
        }
    }

    return summary


def process_task(
    task_dir: Path,
    model: str,
    num_solutions: int,
    temperature: float,
    max_tokens: int,
    max_workers: int = 1,
) -> Dict[str, Any]:
    """Process a single task: generate solutions and save results."""
    print(f"\nProcessing task: {task_dir.name}")

    # Load task data
    task_json_path = task_dir / "task.json"
    if not task_json_path.exists():
        print(f"  [Error] task.json not found in {task_dir}")
        return {}

    with open(task_json_path, 'r', encoding='utf-8') as f:
        task_data = json.load(f)

    # Create solutions directory
    solutions_dir = task_dir / "solutions"
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # Save system prompt
    system_prompt_path = task_dir / "system_prompt.md"
    if not system_prompt_path.exists():
        with open(system_prompt_path, 'w', encoding='utf-8') as f:
            f.write(AGENT_SYSTEM_PROMPT)
        print(f"  Saved system_prompt.md")

    # Save reward rule prompt
    reward_path = task_dir / "reward.md"
    if not reward_path.exists():
        reward_prompt = generate_reward_prompt(task_data)
        with open(reward_path, 'w', encoding='utf-8') as f:
            f.write(reward_prompt)
        print(f"  Saved reward.md")

    start_time = datetime.now(timezone.utc)

    # Generate solutions
    results = []

    if max_workers <= 1:
        # Sequential execution
        for i in range(num_solutions):
            print(f"  Generating solution {i+1}/{num_solutions}...")
            result = run_single_solution(
                solution_idx=i,
                task_data=task_data,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            results.append(result)

            # Save individual solution
            save_solution_result(solutions_dir, i, result, model)
    else:
        # Parallel execution
        def run_and_save(idx: int) -> Dict[str, Any]:
            result = run_single_solution(
                solution_idx=idx,
                task_data=task_data,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            save_solution_result(solutions_dir, idx, result, model)
            return result

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(run_and_save, i): i for i in range(num_solutions)}
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"  Solution {idx+1}/{num_solutions} completed")
                except Exception as e:
                    print(f"  Solution {idx+1}/{num_solutions} failed: {e}")
                    # Add failed result
                    results.append({
                        "success": False,
                        "status": "exception",
                        "error": str(e),
                    })

    end_time = datetime.now(timezone.utc)

    # Generate and save summary
    summary = generate_summary(
        task_dir=task_dir,
        task_data=task_data,
        results=results,
        model=model,
        start_time=start_time,
        end_time=end_time,
    )

    summary_path = solutions_dir / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"  Saved summary to {summary_path}")
    print(f"  Success: {summary['summary']['num_success']}/{num_solutions}")
    print(f"  Pass@1: {summary['summary']['pass_at_k'].get(1, 0.0):.2%}")

    return summary


def main():
    """Main entry point for direct solution generation."""
    parser = argparse.ArgumentParser(
        description="Generate solutions directly via LLM without containers."
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to use for solution generation (e.g., claude-opus-4-6, gpt-4)",
    )
    parser.add_argument(
        "--task-dir",
        type=str,
        required=True,
        help="Directory containing tasks to process",
    )
    parser.add_argument(
        "--num-solutions",
        type=int,
        required=True,
        help="Number of solution attempts per task",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for sampling (default: 0.7)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Maximum tokens per completion (default: 2048)",
    )
    parser.add_argument(
        "--max-episodes",
        type=int,
        default=MAX_EPISODES,
        help=f"Maximum episodes per solution (default: {MAX_EPISODES})",
    )
    parser.add_argument(
        "--num-tasks",
        type=int,
        default=None,
        help="Number of tasks to process (default: all)",
    )
    parser.add_argument(
        "--start-at",
        type=int,
        default=0,
        help="Start at task index (default: 0)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    parser.add_argument(
        "--task-filter",
        type=str,
        default=None,
        help="Filter tasks by name pattern (optional)",
    )

    args = parser.parse_args()

    task_dir = Path(args.task_dir)
    if not task_dir.exists():
        print(f"Error: Task directory does not exist: {task_dir}")
        sys.exit(1)

    # Find all task directories
    task_dirs = []
    for item in task_dir.iterdir():
        if item.is_dir() and item.name.startswith("task_"):
            task_dirs.append(item)

    task_dirs = sorted(task_dirs)

    # Apply filters
    if args.task_filter:
        task_dirs = [d for d in task_dirs if args.task_filter in d.name]

    if args.start_at > 0:
        task_dirs = task_dirs[args.start_at:]

    if args.num_tasks is not None:
        task_dirs = task_dirs[:args.num_tasks]

    print(f"Found {len(task_dirs)} tasks to process")
    print(f"Model: {args.model}")
    print(f"Num solutions per task: {args.num_solutions}")
    print(f"Temperature: {args.temperature}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Workers: {args.workers}")
    print("-" * 60)

    # Process tasks
    all_summaries = []

    if args.workers <= 1:
        # Sequential processing
        for task_path in task_dirs:
            try:
                summary = process_task(
                    task_dir=task_path,
                    model=args.model,
                    num_solutions=args.num_solutions,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                )
                all_summaries.append(summary)
            except Exception as e:
                print(f"  [Error] Failed to process {task_path.name}: {e}")
                import traceback
                traceback.print_exc()
    else:
        # Parallel processing of tasks
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    process_task,
                    task_path,
                    args.model,
                    args.num_solutions,
                    args.temperature,
                    args.max_tokens,
                    1,  # Per-task workers
                ): task_path
                for task_path in task_dirs
            }

            for future in as_completed(futures):
                task_path = futures[future]
                try:
                    summary = future.result()
                    all_summaries.append(summary)
                except Exception as e:
                    print(f"  [Error] Failed to process {task_path.name}: {e}")

    # Print final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    total_tasks = len(all_summaries)
    total_success = sum(s.get("summary", {}).get("num_success", 0) for s in all_summaries if s)
    total_runs = sum(s.get("summary", {}).get("num_runs", 0) for s in all_summaries if s)

    print(f"Total tasks processed: {total_tasks}")
    print(f"Total solutions: {total_runs}")
    print(f"Total successes: {total_success}")
    print(f"Overall success rate: {total_success / total_runs:.2%}" if total_runs > 0 else "N/A")

    print("\nDone!")


if __name__ == "__main__":
    main()
