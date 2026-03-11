"""
Commit command - AI-assisted git commits on the remote server.

Same interface as praisonai commit, but executes git commands on the
remote WordPress server via SSH.
"""

import os
import re

import click
from rich.console import Console

from praisonaiwp.core.config import Config
from praisonaiwp.core.transport import get_transport
from praisonaiwp.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)

# Sensitive patterns (same as praisonai)
_SENSITIVE_FILES = {
    '.env', '.env.local', '.env.production', 'credentials', 'secrets',
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    '.pem', '.key', '.p12', '.pfx', 'credentials', 'secrets.json',
    'secrets.yaml', 'secrets.yml', '.htpasswd', '.netrc',
}
_SENSITIVE_EXTENSIONS = {'.pem', '.key', '.p12', '.pfx', '.jks', '.keystore'}


def _check_sensitive_content(diff_content: str, staged_files: list) -> list:
    """Check for sensitive content in staged changes."""
    issues = []

    for file_path in staged_files:
        file_name = file_path.split('/')[-1].lower()
        if file_name in _SENSITIVE_FILES:
            issues.append((file_path, "Sensitive File", file_name))
            continue
        for ext in _SENSITIVE_EXTENSIONS:
            if file_name.endswith(ext):
                issues.append((file_path, "Sensitive Extension", ext))
                break

    if len(diff_content) < 50000:
        patterns = [
            (re.compile(r"password\s*=\s*['\"]?\w+", re.I), "Password"),
            (re.compile(r"api[_-]?key\s*=\s*['\"]?[\w-]+", re.I), "API Key"),
            (re.compile(r"secret\s*=\s*['\"]?\w+", re.I), "Secret"),
        ]
        for line in diff_content.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                for pattern, issue_type in patterns:
                    if pattern.search(line):
                        matched = pattern.search(line).group(0)[:50] + '...'
                        issues.append(("diff", issue_type, matched))
                        break

    return issues


def _run_git(transport, wp_path: str, cmd: str):
    """Run git command on remote server."""
    full_cmd = f"cd {wp_path} && {cmd}"
    stdout, stderr = transport.execute(full_cmd)
    return stdout, stderr


@click.command()
@click.option('--message', '-m', help='Commit message (AI-generated if not provided)')
@click.option('-a', '--auto', '--all', is_flag=True, help='Full auto: stage all, commit, push (same as praisonai commit -a)')
@click.option('--push', '-p', is_flag=True, help='Push after commit')
@click.option('--no-verify', is_flag=True, help='Skip sensitive content check')
@click.option('--server', default=None, help='Server name from config')
def commit_command(message, auto, push, no_verify, server):
    """
    AI-assisted git commits on the remote server.

    Same as praisonai commit but runs git on the remote WordPress host.
    Use -a for full auto mode: stage all, generate message, commit, push.

    Examples:
        praisonaiwp commit -a
        praisonaiwp commit -m "Update posts"
        praisonaiwp commit --all --push
    """
    try:
        config = Config()
        server_config = config.get_server(server)
        wp_path = server_config.get('wp_path')
        if not wp_path:
            console.print("[red]Server config missing wp_path[/red]")
            raise click.Abort()

        transport = get_transport(config, server)
        transport.connect()

        # Check git repo
        out, err = _run_git(transport, wp_path, "git rev-parse --git-dir 2>/dev/null || echo NOT_GIT")
        if "NOT_GIT" in out or not out.strip():
            console.print("[red]Remote path is not a git repository[/red]")
            raise click.Abort()

        if auto:
            console.print("[cyan]Auto-staging all changes...[/cyan]")
            _run_git(transport, wp_path, "git add -A")

        # Get staged diff
        out, _ = _run_git(transport, wp_path, "git diff --cached --stat")
        if not out.strip():
            # No staged changes - push existing commits if requested
            if push or auto:
                console.print("[cyan]No staged changes; pushing existing commits...[/cyan]")
                _, err = _run_git(transport, wp_path, "git push")
                if err and "Everything up-to-date" not in err and "up to date" not in err.lower():
                    if "no upstream" in err.lower():
                        branch_out, _ = _run_git(transport, wp_path, "git branch --show-current")
                        branch = branch_out.strip() or "master"
                        _, err2 = _run_git(transport, wp_path, f"git push --set-upstream origin {branch}")
                        if err2 and "Everything up-to-date" not in err2:
                            console.print(f"[yellow]Push: {err2}[/yellow]")
                            raise click.Abort()
                    else:
                        console.print(f"[yellow]Push: {err}[/yellow]")
                        raise click.Abort()
                console.print("[green]Pushed to remote[/green]")
                return
            console.print("[yellow]No staged changes. Use -a to stage all first.[/yellow]")
            raise click.Abort()

        diff_out, _ = _run_git(transport, wp_path, "git diff --cached")
        diff_content = (diff_out[:8000] + "...") if len(diff_out) > 8000 else diff_out

        # Security check
        if not no_verify:
            staged_files = [line.split('|')[0].strip() for line in out.strip().split('\n') if '|' in line]
            issues = _check_sensitive_content(diff_out, staged_files)
            if issues and auto:
                console.print("[red]Auto mode aborted: sensitive content detected. Use --no-verify to skip.[/red]")
                for fp, itype, match in issues:
                    console.print(f"  [red]{itype}[/red] in [yellow]{fp}[/yellow]: {match}")
                raise click.Abort()
            elif issues:
                console.print("[bold red]Sensitive content detected[/bold red]")
                for fp, itype, match in issues:
                    console.print(f"  [red]{itype}[/red]: {match}")
                if not click.confirm("Continue anyway?", default=False):
                    raise click.Abort()

        console.print("[bold]Staged changes:[/bold]")
        console.print(out)

        # Resolve commit message
        if message:
            commit_message = message
        else:
            console.print("[bold]Generating commit message...[/bold]")
            try:
                from praisonaiagents import Agent
                agent = Agent(
                    name="CommitMessageGenerator",
                    role="Git Commit Message Writer",
                    goal="Generate clear, concise, conventional commit messages",
                    instructions="""You are an expert at writing git commit messages.
Follow Conventional Commits: feat:, fix:, docs:, chore: etc.
Format: <type>(<scope>): <short description>
Keep first line under 72 chars. Be specific.""",
                    model=os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini"),
                )
                prompt = f"Generate a commit message for these changes:\n\n{out}\n\nDetailed diff:\n{diff_content}\n\nProvide ONLY the commit message, no explanations."
                response = agent.chat(prompt)
                commit_message = (response or "").strip()
                if not commit_message:
                    commit_message = "chore: update multiple files"
                console.print(f"[bold green]Suggested:[/bold green] [cyan]{commit_message}[/cyan]")
                if not auto and not click.confirm("Use this message?", default=True):
                    raise click.Abort()
            except ImportError:
                console.print("[red]Install praisonaiagents for AI messages: pip install praisonaiagents[/red]")
                console.print("Or use -m \"your message\"")
                raise click.Abort()

        # Use base64 to safely pass message to remote (avoids shell escaping)
        import base64
        msg_b64 = base64.b64encode(commit_message.encode('utf-8')).decode('ascii')
        run_cmd = f"echo '{msg_b64}' | base64 -d > /tmp/pw_commit_msg && git commit -F /tmp/pw_commit_msg && rm -f /tmp/pw_commit_msg"
        out, err = _run_git(transport, wp_path, run_cmd)

        err_lower = err.lower()
        if err and "nothing to commit" not in err_lower and "auto packing" not in err_lower:
            console.print(f"[red]{err}[/red]")
            raise click.Abort()

        console.print("[green]Committed successfully[/green]")

        if push or auto:
            out, err = _run_git(transport, wp_path, "git push")
            if err:
                if "no upstream" in err.lower():
                    branch_out, _ = _run_git(transport, wp_path, "git branch --show-current")
                    branch = branch_out.strip() or "master"
                    _, err = _run_git(transport, wp_path, f"git push --set-upstream origin {branch}")
                if err and "Everything up-to-date" not in err:
                    console.print(f"[yellow]Push: {err}[/yellow]")
                else:
                    console.print("[green]Pushed to remote[/green]")
            else:
                console.print("[green]Pushed to remote[/green]")

    except click.Abort:
        raise
    except Exception as e:
        logger.exception("Commit failed")
        console.print(f"[red]{e}[/red]")
        raise click.Abort()
