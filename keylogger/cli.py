# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 CATIE

import os
import sys
import click
import signal
from keylogger.key import MainApp


@click.command()
@click.option(
    "--output",
    type=click.Path(file_okay=False, writable=True),
    default=".",
    help="Output directory for the CSV file.",
)
@click.option(
    "--U",
    is_flag=True,
    help="Capture key up events.",
)
@click.option(
    "--D",
    is_flag=True,
    help="Capture key down events.",
)
@click.option(
    "--key-name/--no-key-name",
    default=True,
    help="Include key name in CSV.",
)
@click.option(
    "--scan-code/--no-scan-code",
    default=True,
    help="Include scan code in CSV.",
)
def cli(output, u, d, key_name, scan_code):
    """Start the keylogger (Ctrl+C to stop)."""

    click.echo("Starting keylogger...")
    app = MainApp(output_dir=output)

    # Configure event types
    app.record_key_down = d or not (u or d)
    app.record_key_up = u or not (u or d)
    app.record_key_name = key_name
    app.record_scan_code = scan_code

    def stop_handler(sig, frame):
        click.echo("Stopping keylogger...")
        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_handler)

    try:
        app.run()
    except KeyboardInterrupt:
        stop_handler(None, None)


if __name__ == "__main__":
    cli()
