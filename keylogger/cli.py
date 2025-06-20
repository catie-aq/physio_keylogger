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
def convert_key_to_csv(output):
    """Start the keylogger (Ctrl+C to stop)."""
    click.echo("Starting keylogger...")
    app = MainApp(output_dir=output)

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
