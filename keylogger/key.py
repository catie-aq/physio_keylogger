# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 CATIE

import time
import logging
import keyboard as kb
import csv
import os
import threading
from datetime import datetime
from typing import Set
from queue import Queue

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class MainApp:
    """Keylogger that logs only to CSV, with optional GUI queue for display."""

    def __init__(
        self,
        output_dir: str = "logs",
        start_time: float = None,
        gui_queue: Queue = None,
    ):
        self.name = "Physio Keylogger"
        self.start_time = start_time if start_time is not None else time.time()
        self.gui_queue = gui_queue
        self._key_press: Set[int] = set()

        self._record_key_down = False
        self._record_key_up = False
        self._record_key_name = False
        self._record_scan_code = False

        self.event_filter: Set[str] = set()
        self._stop_event = threading.Event()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(output_dir, exist_ok=True)
        self.filepath_csv = os.path.join(output_dir, f"keylogger_{timestamp}.csv")

        self._log_file = open(self.filepath_csv, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._log_file)

    @property
    def record_key_down(self) -> bool:
        return self._record_key_down

    @record_key_down.setter
    def record_key_down(self, value: bool) -> None:
        self._record_key_down = value
        if value:
            self.event_filter.add("down")
        else:
            self.event_filter.discard("down")

    @property
    def record_key_up(self) -> bool:
        return self._record_key_up

    @record_key_up.setter
    def record_key_up(self, value: bool) -> None:
        self._record_key_up = value
        if value:
            self.event_filter.add("up")
        else:
            self.event_filter.discard("up")

    @property
    def record_key_name(self) -> bool:
        return self._record_key_name

    @record_key_name.setter
    def record_key_name(self, value: bool) -> None:
        self._record_key_name = value

    @property
    def record_scan_code(self) -> bool:
        return self._record_scan_code

    @record_scan_code.setter
    def record_scan_code(self, value: bool) -> None:
        self._record_scan_code = value

    def _write_headers(self) -> None:
        header = ["timestamp_ms"]
        if self._record_scan_code:
            header.append("scan_code")
        if self._record_key_name:
            header.append("key")
        header.append("event")
        self._writer.writerow(header)
        self._log_file.flush()

    def write(self, key: kb.KeyboardEvent) -> None:
        curr_time = int((key.time - self.start_time) * 1000)
        row = [curr_time]

        if self._record_scan_code:
            row.append(key.scan_code)
        if self._record_key_name:
            row.append(key.name)

        row.append(key.event_type)
        self._writer.writerow(row)
        self._log_file.flush()

        if self.gui_queue:
            try:
                self.gui_queue.put_nowait(f"key: {key.name} ({key.event_type})")
            except:
                pass

    def on_press(self, key: kb.KeyboardEvent) -> None:
        if key.event_type not in self.event_filter:
            return

        if key.event_type == "down":
            if key.scan_code not in self._key_press:
                self._key_press.add(key.scan_code)
                self.write(key)
        elif key.event_type == "up":
            if key.scan_code in self._key_press:
                self._key_press.remove(key.scan_code)
            self.write(key)

    def run(self) -> None:
        self._write_headers()
        kb.hook(self.on_press)
        try:
            while not self._stop_event.is_set():
                time.sleep(0.05)
        finally:
            kb.unhook_all()
            self._log_file.close()

    def stop(self) -> None:
        self._stop_event.set()
