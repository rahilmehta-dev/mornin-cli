import subprocess
from datetime import datetime, timedelta


def parse_since(days=None, since=None):
    if since:
        return since
    d = datetime.now() - timedelta(days=days or 1)
    return d.strftime("%Y-%m-%d")


def get_current_author(repo_path=None):
    cmd = ["git", "config", "user.name"]
    if repo_path:
        cmd = ["git", "-C", str(repo_path)] + cmd[1:]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_git_log(since, author=None, repo_path=None):
    cmd = ["git"]
    if repo_path:
        cmd += ["-C", str(repo_path)]
    cmd += [
        "log",
        f"--since={since}",
        "--pretty=format:%H|%an|%ae|%ad|%s",
        "--date=short",
    ]
    if author:
        cmd.append(f"--author={author}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return None, result.stderr.strip()

    commits = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        parts = line.split("|", 4)
        if len(parts) == 5:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "email": parts[2],
                "date": parts[3],
                "message": parts[4],
            })

    return commits, None
