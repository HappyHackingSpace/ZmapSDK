"""
Command-line interface for ZMap SDK
"""

import logging
import sys

import click

from zmapsdk.api import APIServer
from zmapsdk.core import ZMap


def setup_logging(verbose: bool) -> None:
    """Configure logging with the specified verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def print_version(ctx: click.Context, _, value: bool) -> None:
    """Print ZMap version and exit if --version is specified"""
    if not value or ctx.resilient_parsing:
        return
    try:
        zmap = ZMap()
        version = zmap.get_version()
        click.echo(f"ZMap version: {version}")
    except Exception as e:
        click.echo(f"Warning: Could not detect ZMap version: {e}", err=True)
    ctx.exit()


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show ZMap version and exit.",
)
def cli() -> None:
    """ZMap SDK - Command-line interface for network scanning operations"""
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host address to bind the server to.")
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port number to bind the server to.",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def api(host: str, port: int, verbose: bool) -> None:
    """Run the ZMap SDK API server.

    This command starts a FastAPI-based HTTP server that provides
    a REST API interface to ZMap functionality.
    """
    try:
        setup_logging(verbose)
        server = APIServer(host=host, port=port)
        click.echo(f"Starting ZMap SDK API server on http://{host}:{port}")
        click.echo(f"API documentation available at http://{host}:{port}/docs")
        server.run()
    except Exception as e:
        click.echo(f"Error starting API server: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI"""
    cli(auto_envvar_prefix="ZMAPSDK")


if __name__ == "__main__":
    main()
