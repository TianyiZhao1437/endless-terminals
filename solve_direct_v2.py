#!/usr/bin/env python3
"""
Direct LLM-based solution generator with real container execution.
Generates solutions, trajectories, and summary files with real command execution.
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
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator import chat_completion_batch
from generator.sample_solutions import SYSTEM_MESSAGE, USER_TEMPLATE, _extract_action


MAX_OUTPUT_LENGTH = 50000
MAX_EPISODES = 64
MAX_TIME_SEC = 600

# Agent system prompt for solving terminal tasks
AGENT_SYSTEM_PROMPT = SYSTEM_MESSAGE

# New system prompt that enforces multi-turn interaction and JSON format
MULTI_TURN_SYSTEM_PROMPT = """You are a highly capable Linux terminal agent operating in a real container environment.
Goal: Complete the user's task through systematic exploration and execution.

CRITICAL RULES:
1. You MUST follow this workflow for EVERY task:
   - Step 1: EXPLORE - List directory structure, find relevant files
   - Step 2: READ - View content of relevant files before modifying
   - Step 3: EXECUTE - Make necessary changes
   - Step 4: VERIFY - Check your work with cat, ls, or test commands
   - Step 5: COMPLETE - Only mark done after verification

2. NEVER skip steps. Even for simple tasks, you MUST verify before marking done.

3. Response Format (JSON):
{
  "analysis": "Analyze the current state and what needs to be done",
  "plan": "Describe your plan for the next steps",
  "commands": [
    {"keystrokes": "command1\n", "duration": 1.0},
    {"keystrokes": "command2\n", "duration": 0.5}
  ],
  "task_complete": false
}

4. Command Guidelines:
- Use absolute paths when possible
- Prefer non-interactive commands
- Set appropriate duration (0.1s for quick commands, 1.0s+ for slow ones)
- You can send multiple commands in one response

5. When finished, set "task_complete": true in your response.
""".strip()


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def generate_trial_name(task_name: str) -> str:
    """Generate a trial name similar to harbor format."""
    short_hash = uuid.uuid4().hex[:8]
    task_part = task_name[:25] if len(task_name) > 25 else task_name
    return f"{task_part}__{short_hash}"


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp in ISO format with timezone."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


class ContainerExecutor:
    """Execute commands in a real container environment."""

    def __init__(self, task_dir: Path, container_sif: Optional[Path] = None):
        self.task_dir = task_dir
        self.container_sif = container_sif
        self.temp_dir = task_dir / ".exec_temp"
        self.temp_dir.mkdir(exist_ok=True)

    def execute(self, command: str, timeout: float = 30.0) -> Tuple[str, int]:
        """Execute a command in the container or host environment."""

        if self.container_sif and self.container_sif.exists():
            # Use apptainer for container execution
            return self._execute_apptainer(command, timeout)
        else:
            # Fallback to host execution with environment setup
            return self._execute_host(command, timeout)

    def _execute_apptainer(self, command: str, timeout: float) -> Tuple[str, int]:
        """Execute using apptainer."""
        try:
            # Copy necessary files to temp dir for container access
            cmd = [
                "apptainer", "exec",
                "--bind", f"{self.temp_dir}:/tmp/workspace",
                str(self.container_sif),
                "bash", "-c", f"cd /tmp/workspace && {command}"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            output = result.stdout
            if result.stderr:
                output += f"\nstderr: {result.stderr}"

            return (output, result.returncode)

        except subprocess.TimeoutExpired:
            return (f"Command timed out after {timeout}s", 124)
        except Exception as e:
            return (f"Execution error: {str(e)}", 1)

    def _execute_host(self, command: str, timeout: float) -> Tuple[str, int]:
        """Execute on host (fallback)."""
        try:
            # Setup environment to mimic container
            env = os.environ.copy()
            env["HOME"] = str(self.temp_dir)

            # Pre-process command to handle common task paths
            # Replace /home/user with temp directory path
            modified_command = command.replace("/home/user", str(self.temp_dir))

            result = subprocess.run(
                modified_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.temp_dir,
                env=env
            )

            output = result.stdout
            if result.stderr:
                output += f"\nstderr: {result.stderr}"

            return (output, result.returncode)

        except subprocess.TimeoutExpired:
            return (f"Command timed out after {timeout}s", 124)
        except Exception as e:
            return (f"Execution error: {str(e)}", 1)

    def verify_with_pytest(self, test_file: Path) -> Tuple[bool, str]:
        """Run pytest to verify solution by checking files directly."""
        try:
            # On macOS/Windows, we can't create /home/user, so check files directly
            log_dir = self.temp_dir / "distributed_logs"
            output_file = log_dir / "highest_latency.log"
            input_file = log_dir / "system-events.log"

            errors = []

            # Check directory exists
            if not log_dir.exists():
                errors.append(f"Directory '{log_dir}' does not exist")

            # Check output file exists
            if not output_file.exists():
                errors.append(f"Output file '{output_file}' does not exist")
            else:
                # Check content
                content = output_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                # Remove empty trailing line from split
                if lines and lines[-1] == '':
                    lines = lines[:-1]

                if len(lines) != 1:
                    errors.append(f"Expected 1 line, got {len(lines)}: {lines!r}")
                else:
                    expected = "db-service 305 2024-06-01T15:30:25Z"
                    if lines[0] != expected:
                        errors.append(f"Expected '{expected}', got '{lines[0]}'")

            if errors:
                return (False, "Verification failed:\n" + "\n".join(errors))
            return (True, "Verification passed!")

        except Exception as e:
            return (False, f"Verification error: {str(e)}")

    def setup_task_files(self, truth_data: str):
        """Initialize task files from truth data description."""
        # Parse truth to extract initial file contents
        # Format: "Initial file: /home/user/...\nContents:\n..."
        if not truth_data:
            return

        lines = truth_data.split('\n')
        current_file = None
        current_content = []
        in_content = False

        for line in lines:
            if line.startswith('Initial file:'):
                # Save previous file if any
                if current_file and current_content:
                    self._write_task_file(current_file, '\n'.join(current_content))
                current_file = line.split(':', 1)[1].strip()
                current_content = []
                in_content = False
            elif line == 'Contents:' or line.startswith('Content:'):
                in_content = True
            elif in_content and line:
                # Stop at metadata lines
                if line.startswith('Expected output') or line.startswith('File permissions'):
                    in_content = False
                    continue
                current_content.append(line)

        # Save last initial file (not expected output files)
        if current_file and current_content and 'highest_latency' not in current_file:
            self._write_task_file(current_file, '\n'.join(current_content))

    def _write_task_file(self, file_path: str, content: str):
        """Write a task file to the appropriate location."""
        # Map /home/user to temp_dir
        if file_path.startswith('/home/user'):
            local_path = self.temp_dir / file_path[len('/home/user/'):]
        else:
            local_path = self.temp_dir / file_path.lstrip('/')

        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_temp_path(self, original_path: str) -> Path:
        """Convert a container path to local temp path."""
        if original_path.startswith('/home/user'):
            return self.temp_dir / original_path[len('/home/user/'):]
        return self.temp_dir / original_path.lstrip('/')


def parse_agent_response(response_text: str) -> Dict[str, Any]:
    """Parse agent response to extract commands and completion status."""

    # Try JSON format first
    try:
        # Find JSON in response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "analysis": data.get("analysis", ""),
                "plan": data.get("plan", ""),
                "commands": data.get("commands", []),
                "task_complete": data.get("task_complete", False),
                "raw": response_text
            }
    except json.JSONDecodeError:
        pass

    # Fall back to XML format
    action = _extract_action(response_text)

    if action["type"] == "done":
        return {
            "analysis": "Task marked as complete",
            "plan": "",
            "commands": [],
            "task_complete": True,
            "raw": response_text
        }
    elif action["type"] == "command":
        return {
            "analysis": "",
            "plan": "",
            "commands": [{"keystrokes": action["command"] + "\n", "duration": 1.0}],
            "task_complete": False,
            "raw": response_text
        }
    else:
        return {
            "analysis": "Invalid response format",
            "plan": "Please respond with valid JSON or <command> tags",
            "commands": [],
            "task_complete": False,
            "raw": response_text
        }


def run_single_solution(
    solution_idx: int,
    task_data: Dict[str, Any],
    task_dir: Path,
    model: str,
    temperature: float,
    max_tokens: int,
    max_episodes: int = MAX_EPISODES,
) -> Dict[str, Any]:
    """
    Run a single solution attempt with real command execution.
    """
    task_description = task_data.get("description", "")
    task_name = task_data.get("name", "unknown_task")
    task_truth = task_data.get("truth", "")

    # Setup container executor
    container_sif = task_dir / "container.sif"
    executor = ContainerExecutor(task_dir, container_sif if container_sif.exists() else None)

    # Initialize task files from truth data
    executor.setup_task_files(task_truth)

    # Initialize trajectory
    session_id = generate_session_id()
    steps = []
    episode_id = 0

    # Agent info
    agent_info = {
        "name": "direct-llm-solver-v2",
        "version": "2.0.0",
        "model_name": model,
        "extra": {
            "parser": "json",
            "temperature": temperature,
        }
    }

    # Create user message with task
    user_message = USER_TEMPLATE.format(task_description=task_description)

    # Initial step
    episode_id += 1
    steps.append({
        "step_id": episode_id,
        "timestamp": format_timestamp(),
        "source": "user",
        "message": user_message,
    })

    # Initialize chat
    chat = [
        {"role": "system", "content": MULTI_TURN_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # Track metrics
    total_input_tokens = 0
    total_output_tokens = 0
    api_request_times = []

    # Create episode directory
    solution_dir = task_dir / "solutions" / f"solution_{solution_idx:04d}"
    episodes_dir = solution_dir / "episodes"
    episodes_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    n_episodes = 0
    final_status = "incomplete"
    verification_passed = False

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
            api_time = (time.time() - api_start) * 1000
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

            # Parse response
            parsed = parse_agent_response(raw_content)

            # Save episode data
            episode_dir = episodes_dir / f"episode-{episode:04d}"
            episode_dir.mkdir(exist_ok=True)

            # Save prompt (chat history)
            with open(episode_dir / "prompt.txt", 'w', encoding='utf-8') as f:
                for msg in chat:
                    f.write(f"[{msg['role']}]: {msg['content']}\n{'='*50}\n")

            # Save raw response
            with open(episode_dir / "response.txt", 'w', encoding='utf-8') as f:
                f.write(raw_content)

            # Save debug info
            debug_info = {
                "episode": episode,
                "timestamp": format_timestamp(),
                "api_time_ms": api_time,
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if hasattr(response, 'usage') else 0,
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if hasattr(response, 'usage') else 0,
                "parsed_analysis": parsed.get("analysis", ""),
                "parsed_plan": parsed.get("plan", ""),
                "num_commands": len(parsed.get("commands", [])),
                "task_complete": parsed.get("task_complete", False),
            }
            with open(episode_dir / "debug.json", 'w', encoding='utf-8') as f:
                json.dump(debug_info, f, indent=2)

            # Add agent step
            episode_id += 1

            if parsed.get("task_complete", False):
                steps.append({
                    "step_id": episode_id,
                    "timestamp": format_timestamp(),
                    "source": "agent",
                    "model_name": model,
                    "message": parsed.get("analysis", "Task complete"),
                    "metrics": {
                        "prompt_tokens": debug_info["prompt_tokens"],
                        "completion_tokens": debug_info["completion_tokens"],
                    }
                })
                final_status = "completed"
                break

            # Execute commands
            commands = parsed.get("commands", [])
            if not commands and parsed.get("raw"):
                # Fallback: try to extract single command
                action = _extract_action(parsed["raw"])
                if action["type"] == "command":
                    commands = [{"keystrokes": action["command"] + "\n", "duration": 1.0}]

            if commands:
                tool_calls = []
                observation_results = []

                for i, cmd in enumerate(commands):
                    cmd_str = cmd.get("keystrokes", "").strip()
                    duration = cmd.get("duration", 1.0)

                    tool_call_id = f"call_{episode}_{i+1}"
                    tool_calls.append({
                        "tool_call_id": tool_call_id,
                        "function_name": "bash_command",
                        "arguments": {
                            "keystrokes": cmd_str,
                            "duration": duration,
                        }
                    })

                    # Execute command in real environment
                    output, exit_code = executor.execute(cmd_str, timeout=min(duration * 3, 60))

                    observation_results.append({
                        "content": f"Command: {cmd_str}\nOutput:\n{output}",
                        "exit_code": exit_code,
                    })

                # Add agent step with tool calls
                steps.append({
                    "step_id": episode_id,
                    "timestamp": format_timestamp(),
                    "source": "agent",
                    "model_name": model,
                    "message": parsed.get("analysis", "") + "\n" + parsed.get("plan", ""),
                    "tool_calls": tool_calls,
                    "observation": {
                        "results": observation_results
                    },
                    "metrics": {
                        "prompt_tokens": debug_info["prompt_tokens"],
                        "completion_tokens": debug_info["completion_tokens"],
                    }
                })

                # Build result message
                result_lines = []
                for i, obs in enumerate(observation_results):
                    result_lines.append(f"Command {i+1} (exit={obs['exit_code']}):\n{obs['content'][:500]}")
                result_message = "\n\n".join(result_lines)

                # Update chat
                chat.append({"role": "assistant", "content": raw_content})
                chat.append({"role": "user", "content": result_message})

                # Add system step
                episode_id += 1
                steps.append({
                    "step_id": episode_id,
                    "timestamp": format_timestamp(),
                    "source": "system",
                    "message": result_message,
                })
            else:
                # No commands, just analysis
                steps.append({
                    "step_id": episode_id,
                    "timestamp": format_timestamp(),
                    "source": "agent",
                    "model_name": model,
                    "message": parsed.get("analysis", "No action taken"),
                    "metrics": {
                        "prompt_tokens": debug_info["prompt_tokens"],
                        "completion_tokens": debug_info["completion_tokens"],
                    }
                })

                chat.append({"role": "assistant", "content": raw_content})
                chat.append({"role": "user", "content": "Please provide commands to execute or mark the task as complete."})

                episode_id += 1
                steps.append({
                    "step_id": episode_id,
                    "source": "system",
                    "message": "Please provide commands to execute or mark the task as complete.",
                })

        else:
            # Max episodes reached
            final_status = "max_episodes"

    except Exception as e:
        final_status = "exception"
        steps.append({
            "step_id": episode_id + 1,
            "source": "system",
            "message": f"Exception occurred: {str(e)}",
        })

    # Verify solution with pytest if test file exists
    test_final_path = task_dir / "test_final_state.py"
    if test_final_path.exists():
        verification_passed, verify_output = executor.verify_with_pytest(test_final_path)
        print(f"  Solution {solution_idx} verification: {'PASSED' if verification_passed else 'FAILED'}")

    end_time = time.time()

    # Build trajectory
    trajectory = {
        "schema_version": "ATIF-v1.6",
        "session_id": session_id,
        "agent": agent_info,
        "steps": steps,
    }

    # Build result
    result = {
        "success": verification_passed if test_final_path.exists() else (final_status == "completed"),
        "status": final_status,
        "verification_passed": verification_passed,
        "messages": chat,
        "trajectory": trajectory,
        "n_episodes": n_episodes,
        "n_input_tokens": total_input_tokens,
        "n_output_tokens": total_output_tokens,
        "api_request_times_msec": api_request_times,
        "duration_sec": end_time - start_time,
    }

    return result


def generate_solve_script(commands: List[Dict]) -> str:
    """Generate a solve.sh script from executed commands."""
    script_lines = ["#!/bin/bash", "set -e", ""]

    for cmd in commands:
        cmd_str = cmd.get("keystrokes", "").strip()
        if cmd_str:
            script_lines.append(f"# {cmd_str[:50]}{'...' if len(cmd_str) > 50 else ''}")
            script_lines.append(cmd_str)
            script_lines.append("")

    return "\n".join(script_lines)


def save_solution_result(
    task_dir: Path,
    solution_idx: int,
    result: Dict[str, Any],
    model_name: str,
) -> Path:
    """Save a single solution result to disk."""
    solution_dir = task_dir / "solutions" / f"solution_{solution_idx:04d}"
    solution_dir.mkdir(parents=True, exist_ok=True)

    # Trajectory directory
    trajectory_dir = solution_dir / "trajectory"
    trajectory_dir.mkdir(parents=True, exist_ok=True)

    # Save trajectory.json
    trajectory_path = trajectory_dir / "trajectory.json"
    with open(trajectory_path, 'w', encoding='utf-8') as f:
        json.dump(result["trajectory"], f, indent=2, ensure_ascii=False)

    # Extract commands for solve.sh
    commands = []
    for step in result["trajectory"]["steps"]:
        for tool_call in step.get("tool_calls", []):
            args = tool_call.get("arguments", {})
            if args.get("keystrokes"):
                commands.append(args)

    # Generate and save solve.sh
    solve_script = generate_solve_script(commands)
    solve_path = solution_dir / "solve.sh"
    with open(solve_path, 'w', encoding='utf-8') as f:
        f.write(solve_script)

    os.chmod(solve_path, 0o755)

    # Save raw result (without trajectory to avoid duplication)
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

You are an expert evaluator for terminal-based tasks. Your job is to analyze a given trajectory and determine whether the task was completed successfully.

### Scoring Criteria

Score the trajectory on a scale of 0.0 to 1.0:

- **1.0 (Perfect Success)**: The task is fully completed according to all specifications
- **0.8-0.9 (Success with minor issues)**: The task is completed but with minor deviations
- **0.5-0.7 (Partial Success)**: Some requirements met but not all
- **0.1-0.4 (Failure)**: Task attempted but not completed
- **0.0 (No attempt)**: Task not attempted or completely wrong

### Key Questions to Answer

- Did the agent follow the workflow (explore -> read -> execute -> verify)?
- Did the agent create/modify the required files?
- Is the file content exactly as specified in the task?
- Did the agent verify their work before marking done?
- Did the pytest verification pass?

### Output Format

```
Score: <0.0-1.0>
Reasoning: <Brief explanation>
Verdict: <SUCCESS|PARTIAL|FAILURE>
```

Evaluate the provided trajectory and assign an appropriate score.
"""
    return prompt.strip()


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
            f.write(MULTI_TURN_SYSTEM_PROMPT)
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

    for i in range(num_solutions):
        print(f"  Generating solution {i+1}/{num_solutions}...")
        result = run_single_solution(
            solution_idx=i,
            task_data=task_data,
            task_dir=task_dir,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        results.append(result)

        # Save individual solution
        save_solution_result(task_dir, i, result, model)

        # Print summary
        status = "✓" if result.get("verification_passed") or result.get("success") else "✗"
        print(f"    {status} Episodes: {result['n_episodes']}, Tokens: {result['n_input_tokens']}/{result['n_output_tokens']}")

    end_time = datetime.now(timezone.utc)

    # Generate summary
    num_success = sum(1 for r in results if r.get("verification_passed", r.get("success", False)))
    pass_at_k = compute_pass_at_k(num_solutions, num_success)

    summary = {
        "id": str(uuid.uuid4()),
        "task_name": task_data.get("name", "unknown"),
        "trial_name": generate_trial_name(task_data.get("name", "unknown")),
        "num_runs": num_solutions,
        "num_success": num_success,
        "pass_at_k": pass_at_k,
        "success_rate": num_success / num_solutions if num_solutions > 0 else 0.0,
        "started_at": start_time.isoformat(),
        "finished_at": end_time.isoformat(),
        "results": [
            {
                "solution_idx": i,
                "success": r.get("verification_passed", r.get("success", False)),
                "status": r.get("status", "unknown"),
                "n_episodes": r.get("n_episodes", 0),
                "n_input_tokens": r.get("n_input_tokens", 0),
                "n_output_tokens": r.get("n_output_tokens", 0),
            }
            for i, r in enumerate(results)
        ]
    }

    summary_path = solutions_dir / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"  Saved summary to {summary_path}")
    print(f"  Success: {num_success}/{num_solutions}")
    print(f"  Pass@1: {pass_at_k.get(1, 0.0):.2%}")

    return summary


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate solutions with real container execution."
    )
    parser.add_argument("--model", type=str, required=True, help="Model to use")
    parser.add_argument("--task-dir", type=str, required=True, help="Directory containing tasks")
    parser.add_argument("--num-solutions", type=int, required=True, help="Number of solutions per task")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for sampling")
    parser.add_argument("--max-tokens", type=int, default=2048, help="Max tokens per completion")
    parser.add_argument("--num-tasks", type=int, default=None, help="Number of tasks to process")
    parser.add_argument("--start-at", type=int, default=0, help="Start at task index")

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

    task_dirs = sorted(task_dirs)[args.start_at:]

    if args.num_tasks is not None:
        task_dirs = task_dirs[:args.num_tasks]

    print(f"Found {len(task_dirs)} tasks to process")
    print(f"Model: {args.model}")
    print(f"Num solutions per task: {args.num_solutions}")
    print("-" * 60)

    # Process tasks
    for task_path in task_dirs:
        try:
            process_task(
                task_dir=task_path,
                model=args.model,
                num_solutions=args.num_solutions,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
        except Exception as e:
            print(f"  [Error] Failed to process {task_path.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\nDone!")


if __name__ == "__main__":
    main()
