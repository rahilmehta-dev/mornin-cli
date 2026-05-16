# mornin

**Morning standup summaries from your git history — powered by a local LLM.**

No cloud. No API keys. Runs entirely on your machine via [Ollama](https://ollama.ai).

[![PyPI version](https://img.shields.io/pypi/v/mornin)](https://pypi.org/project/mornin)
[![Python](https://img.shields.io/pypi/pyversions/mornin)](https://pypi.org/project/mornin)

---

![mornin demo](assets/demo.png)

---

## Install

```bash
pip install mornin
```

**Requirements:**
- [Ollama](https://ollama.ai) installed and running
- A model pulled — `ollama pull llama3.1:8b` is a good start

---

## Quick Start

```bash
cd your-project
mornin setup          # configure once
mornin                # summarize yesterday's commits
```

---

## Commands

### Summarize commits

```bash
mornin                        # yesterday (default)
mornin --days 7               # last 7 days
mornin --since "last monday"  # natural date string
mornin --model qwen2.5:3b     # override model for this run
```

### Report mode

Formats output as a clean bullet list — ready to paste into Slack or email.

```bash
mornin --days 7 --report
```

![report output](assets/report.png)

```
May 9 – May 16, 2026

ShowUp
  • Fixed daily reset and timer bugs
  • Added task status badges and unit tests
  • Set up GitHub Actions

mornin-cli
  • Started the project, made initial commit
```

---

## Multiple Repos

Track multiple projects and summarize them all at once with `--all`.

### 1. Add repos to your list

```bash
mornin add-repo                        # adds current directory
mornin add-repo ~/code/my-other-app   # adds a specific path
```

Repos are saved to `~/.mornin/config.json` and reused every time you run `--all`.

![add-repo](assets/add-repo.png)

### 2. Summarize all repos

```bash
mornin --all
mornin --all --days 7
mornin --all --report
```

![all repos output](assets/all.png)

Output is grouped by repo name automatically.

---

## Configuration

Run `mornin setup` for interactive setup, or edit `~/.mornin/config.json` directly.

```bash
mornin setup
```

![setup](assets/setup.png)

| Key             | Default                  | Description                              |
|-----------------|--------------------------|------------------------------------------|
| `endpoint`      | `http://localhost:11434` | Ollama API endpoint                      |
| `model`         | `llama3.2`               | Model used for summarization             |
| `days`          | `1`                      | Default look-back window in days         |
| `format`        | `bullet`                 | Output format: `bullet` or `paragraph`   |
| `author_filter` | `true`                   | Only include your own commits            |
| `repos`         | `[]`                     | Repo paths used with `--all`             |

---

## How It Works

1. Runs `git log` in the target repo(s) with your configured date range
2. Filters commits by your git `user.name` (if `author_filter` is enabled)
3. Sends the commit messages to your local Ollama model
4. Prints a clean summary — no data ever leaves your machine

---

## License

MIT
