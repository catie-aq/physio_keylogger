# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 CATIE

import time
import logging
import keyboard as kb
import csv
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainApp:
    """keylogger application."""

    def __init__(self, output_dir="."):
        self.name = "Physio Keylogger"
        self.start_time = time.time()
        self.key_press = []

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"keylogger_{timestamp}.csv"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        self.log_file = open(filepath, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.log_file)
        self.writer.writerow(["timestamp_ms", "scan_code", "key", "event"])
        logger.info("Logging to %s", filepath)

    def write(self, key):
        """Write key event to CSV file."""
        curr_time = int((key.time - self.start_time) * 1000)
        self.writer.writerow([curr_time, key.scan_code, key.name, key.event_type])
        self.log_file.flush()
        logger.info("Logged key: %s (%s)", key.name, key.event_type)

    def on_press(self, key):
        """Handle key press events."""
        if key.event_type == "down" and key.scan_code not in self.key_press:
            self.key_press.append(key.scan_code)
            self.write(key)
        elif key.event_type == "up" and key.scan_code in self.key_press:
            self.key_press.remove(key.scan_code)
            self.write(key)

    def run(self):
        """Start the keylogger."""
        logger.info("Starting %s...", self.name)
        kb.hook(self.on_press)
        kb.wait()
        self.log_file.close()


def main():
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()
