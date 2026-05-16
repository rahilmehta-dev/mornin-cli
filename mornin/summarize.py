import requests


def build_prompt(commits_by_repo, fmt):
    format_instruction = (
        "Format the summary as concise bullet points."
        if fmt == "bullet"
        else "Format the summary as a short paragraph."
    )

    sections = []
    for repo, commits in commits_by_repo.items():
        lines = "\n".join(
            f"  - [{c['date']}] {c['message']}" for c in commits
        )
        sections.append(f"{repo}:\n{lines}")

    body = "\n\n".join(sections)
    return (
        f"Summarize the following git commits into a morning standup update. "
        f"Write in first person. Never mention any author's name. "
        f"{format_instruction} Group the summary by repository.\n\nCommits:\n{body}\n\nSummary:"
    )


def format_report(commits_by_repo):
    sections = []
    for repo, commits in commits_by_repo.items():
        bullets = "\n".join(f"  • {c['message']}" for c in commits)
        sections.append(f"{repo}\n{bullets}")
    return "\n\n".join(sections)


def _call_ollama(prompt, config):
    url = f"{config['endpoint'].rstrip('/')}/api/generate"
    payload = {"model": config["model"], "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json().get("response", "").strip()


def summarize(commits_by_repo, config):
    if not commits_by_repo:
        return "No commits found in the given time range."
    return _call_ollama(build_prompt(commits_by_repo, config.get("format", "bullet")), config)


def summarize_report(commits_by_repo):
    if not commits_by_repo:
        return "No commits found in the given time range."
    return format_report(commits_by_repo)
