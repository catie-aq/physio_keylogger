# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 CATIE

import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import os
import sys
import time
import csv
import keyboard
from datetime import datetime


class PrintRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, msg):
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, msg)
        self.textbox.see(tk.END)
        self.textbox.configure(state="disabled")

    def flush(self):
        pass


class KeyloggerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keylogger GUI")
        self.geometry("600x400")
        self.output_dir = tk.StringVar(value=os.getcwd())
        self.is_running = False
        self.log_file = None
        self.key_press = []
        self.start_time = time.time()
        self.writer = None
        self.record_key_up = tk.BooleanVar(value=False)
        self.record_key_down = tk.BooleanVar(value=True)
        self.record_key_name = tk.BooleanVar(value=False)
        self.record_scan_code = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Output directory
        tk.Label(self, text="Output Directory:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        tk.Entry(self, textvariable=self.output_dir, width=50).grid(
            row=0, column=1, padx=5, pady=5
        )
        tk.Button(self, text="Browse", command=self.browse_output_dir).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Checkboxes for event types
        checkbox_frame = tk.Frame(self)
        checkbox_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.down_checkbox = tk.Checkbutton(
            checkbox_frame, text="Key Down", variable=self.record_key_down
        )
        self.down_checkbox.pack(side="left", padx=5)

        self.up_checkbox = tk.Checkbutton(
            checkbox_frame, text="Key Up", variable=self.record_key_up
        )
        self.up_checkbox.pack(side="left", padx=5)

        self.keyname_checkbox = tk.Checkbutton(
            checkbox_frame, text="Key Name", variable=self.record_key_name
        )
        self.keyname_checkbox.pack(side="left", padx=5)

        self.scancode_checkbox = tk.Checkbutton(
            checkbox_frame, text="Scan Code", variable=self.record_scan_code
        )
        self.scancode_checkbox.pack(side="left", padx=5)

        # Start and Stop buttons
        self.start_btn = tk.Button(self, text="Start", command=self.start_logging)
        self.start_btn.grid(row=3, column=1, padx=(5, 2), pady=5, sticky="e")
        self.stop_btn = tk.Button(
            self, text="Stop", command=self.stop_logging, state="disabled"
        )
        self.stop_btn.grid(row=3, column=2, padx=(2, 5), pady=5, sticky="w")

        # Text output
        self.textbox = scrolledtext.ScrolledText(self, height=15, state="disabled")
        self.textbox.grid(
            row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew"
        )

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def browse_output_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def start_logging(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.up_checkbox.config(state="disabled")
        self.down_checkbox.config(state="disabled")
        self.keyname_checkbox.config(state="disabled")
        self.scancode_checkbox.config(state="disabled")

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.configure(state="disabled")

        threading.Thread(target=self.run_logging, daemon=True).start()

    def run_logging(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"keylogger_{timestamp}.csv"
        filepath = os.path.join(self.output_dir.get(), filename)

        try:
            self.log_file = open(filepath, "w", newline="", encoding="utf-8")
            self.writer = csv.writer(self.log_file)
            header = ["timestamp_ms"]
            if self.record_scan_code.get():
                header.append("scan_code")
            if self.record_key_name.get():
                header.append("key")
            header.append("event")
            self.writer.writerow(header)

            sys.stdout = sys.stderr = PrintRedirector(self.textbox)
            print(f"Logging to {filepath}")

            def on_key_event(key):
                if not self.is_running:
                    return
                if key.event_type == "up" and not self.record_key_up.get():
                    return
                if key.event_type == "down" and not self.record_key_down.get():
                    return
                curr_time = int((key.time - self.start_time) * 1000)
                row = [curr_time]
                if self.record_scan_code.get():
                    row.append(key.scan_code)
                if self.record_key_name.get():
                    row.append(key.name)
                row.append(key.event_type)
                if key.event_type == "down" and key.scan_code not in self.key_press:
                    self.key_press.append(key.scan_code)
                elif key.event_type == "up" and key.scan_code in self.key_press:
                    self.key_press.remove(key.scan_code)
                self.writer.writerow(row)
                self.log_file.flush()
                print(f"{key.name} ({key.event_type})")

            keyboard.hook(on_key_event)
            keyboard.wait()

        except Exception as e:
            print(f"Error: {e}")

    def stop_logging(self):
        if not self.is_running:
            return
        self.is_running = False
        keyboard.unhook_all()
        if self.log_file:
            self.log_file.close()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.up_checkbox.config(state="normal")
        self.down_checkbox.config(state="normal")
        self.keyname_checkbox.config(state="normal")
        self.scancode_checkbox.config(state="normal")
        print("Logging stopped.")


def main():
    app = KeyloggerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
