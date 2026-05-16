import click
from .config import load_config, save_config


def run_setup():
    config = load_config()

    click.echo("Configure mornin — press Enter to keep the current value.\n")

    endpoint = click.prompt("Ollama endpoint", default=config["endpoint"])
    model = click.prompt("Model", default=config["model"])
    days = click.prompt("Default days to look back", default=config["days"], type=int)
    fmt = click.prompt(
        "Output format",
        default=config["format"],
        type=click.Choice(["bullet", "paragraph"]),
    )
    author_filter = click.confirm(
        "Filter commits by git user.name?",
        default=config["author_filter"],
    )

    save_config({
        **config,
        "endpoint": endpoint,
        "model": model,
        "days": days,
        "format": fmt,
        "author_filter": author_filter,
    })

    click.echo("\nConfig saved to ~/.mornin/config.json")
