from datetime import datetime
from pathlib import Path

import click

from .config import load_config, save_config
from .git import get_git_log, get_current_author, parse_since
from .summarize import summarize, summarize_report
from .setup import run_setup


def _format_date_range(since_str):
    start = datetime.strptime(since_str, "%Y-%m-%d")
    end = datetime.now()
    return f"{start.strftime('%b %-d')} – {end.strftime('%b %-d, %Y')}"


def _print_header(since_str):
    date_range = _format_date_range(since_str)
    title = f"  Morning Standup · {date_range}  "
    bar = "─" * len(title)
    click.echo(click.style(f"╭{bar}╮", fg="bright_blue"))
    click.echo(click.style("│", fg="bright_blue") + click.style(title, fg="white", bold=True) + click.style("│", fg="bright_blue"))
    click.echo(click.style(f"╰{bar}╯", fg="bright_blue"))
    click.echo()


def _collect(repos, since_str, author):
    commits_by_repo = {}
    for repo in repos:
        path = Path(repo).expanduser().resolve()
        commits, err = get_git_log(since_str, author=author, repo_path=path)
        if err:
            click.echo(f"git error ({path.name}): {err}", err=True)
            continue
        if commits:
            commits_by_repo[path.name] = commits
    return commits_by_repo


@click.group(invoke_without_command=True)
@click.option("--days", default=None, type=int, help="Number of days to look back.")
@click.option("--since", default=None, type=str, help="Date string (e.g. 'last monday').")
@click.option("--model", default=None, type=str, help="Override Ollama model for this run.")
@click.option("--all", "use_all", is_flag=True, default=False, help="Summarize all repos in config.")
@click.option("--report", is_flag=True, default=False, help="Clean report format for Slack or email.")
@click.pass_context
def cli(ctx, days, since, model, use_all, report):
    """Summarize your git activity for the morning standup."""
    if ctx.invoked_subcommand is not None:
        return

    config = load_config()

    if model:
        config["model"] = model

    effective_days = days if days is not None else config["days"]
    since_str = parse_since(days=effective_days, since=since)

    author = None
    if config.get("author_filter"):
        author = get_current_author()

    if use_all:
        repos = config.get("repos", [])
        if not repos:
            click.echo("No repos in config. Add one with: mornin add-repo [path]", err=True)
            raise SystemExit(1)
        commits_by_repo = _collect(repos, since_str, author)
    else:
        cwd = str(Path.cwd())
        commits, err = get_git_log(since_str, author=author)
        if err:
            click.echo(f"git error: {err}", err=True)
            raise SystemExit(1)
        commits_by_repo = {Path(cwd).name: commits} if commits else {}

    if not commits_by_repo:
        label = f"author '{author}'" if author else "any author"
        click.echo(f"No commits found since {since_str} for {label}.")
        return

    total = sum(len(c) for c in commits_by_repo.values())
    click.echo(click.style(f"↻ Summarizing {total} commit(s) across {len(commits_by_repo)} repo(s) since {since_str}...", fg="bright_black"), err=True)
    click.echo()

    try:
        if report:
            _print_header(since_str)
            click.echo(summarize_report(commits_by_repo))
        else:
            _print_header(since_str)
            click.echo(summarize(commits_by_repo, config))
    except Exception as e:
        click.echo(f"Ollama error: {e}", err=True)
        raise SystemExit(1)


@cli.command()
def setup():
    """Interactive config setup."""
    run_setup()


@cli.command("add-repo")
@click.argument("path", default=".", required=False)
def add_repo(path):
    """Add a repo to the --all list. Defaults to current directory."""
    resolved = str(Path(path).expanduser().resolve())
    config = load_config()
    repos = config.get("repos", [])
    if resolved in repos:
        click.echo(f"Already in list: {resolved}")
        return
    repos.append(resolved)
    config["repos"] = repos
    save_config(config)
    click.echo(f"Added: {resolved}")
