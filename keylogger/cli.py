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
def convert_key_to_csv(output, u, d):
    """Start the keylogger (Ctrl+C to stop)."""
    event_filter = set()
    if u:
        event_filter.add("up")
    if d:
        event_filter.add("down")
    if not event_filter:
        event_filter = {"up", "down"}

    click.echo(f"Starting keylogger with events: {', '.join(event_filter)}")
    app = MainApp(output_dir=output, event_filter=event_filter)

    def stop_handler(sig, frame):
        click.echo("Stopping keylogger...")
        app.log_file.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_handler)

    try:
        app.run()
    except KeyboardInterrupt:
        stop_handler(None, None)


if __name__ == "__main__":
    convert_key_to_csv()
