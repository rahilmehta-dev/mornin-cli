# mornin

Morning standup CLI — summarize your recent git commits using a local LLM via [Ollama](https://ollama.ai).

## Install

```bash
pip install mornin
```

## Requirements

- [Ollama](https://ollama.ai) running locally (default: `http://localhost:11434`)
- A pulled model, e.g. `ollama pull llama3.2`

## Usage

```bash
mornin                        # summarize yesterday's commits
mornin --days 3               # last 3 days
mornin --since "last monday"  # commits since a date string
mornin --model qwen2.5:3b     # override model for this run
mornin setup                  # interactive config setup
```

## Config

Stored at `~/.mornin/config.json`. Run `mornin setup` to configure interactively.

| Key             | Default                     | Description                              |
|-----------------|-----------------------------|------------------------------------------|
| `endpoint`      | `http://localhost:11434`    | Ollama API endpoint                      |
| `model`         | `llama3.2`                  | Model to use for summarization           |
| `days`          | `1`                         | Default days to look back                |
| `format`        | `bullet`                    | Output format: `bullet` or `paragraph`   |
| `author_filter` | `true`                      | Filter commits to `git config user.name` |
