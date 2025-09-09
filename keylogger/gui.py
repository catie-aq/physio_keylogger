# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 CATIE

import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import os
import time
from queue import Queue, Empty

from keylogger.key import MainApp


class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Physio Keylogger")

        self.output_dir = tk.StringVar(
            value=os.path.expanduser("~/Documents/physio_keylogger")
        )
        self.var_key_down = tk.BooleanVar(value=True)
        self.var_key_up = tk.BooleanVar(value=False)
        self.var_key_name = tk.BooleanVar(value=True)
        self.var_scan_code = tk.BooleanVar(value=True)

        self.global_start_time = None
        self.logger_thread = None
        self.app = None
        self.gui_queue = Queue()

        tk.Label(master, text="Output Directory:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        self.dir_entry = tk.Entry(master, textvariable=self.output_dir, width=60)
        self.dir_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_directory).grid(
            row=0, column=4, padx=5
        )

        tk.Checkbutton(master, text="Key Down", variable=self.var_key_down).grid(
            row=1, column=0, sticky="w", padx=10
        )
        tk.Checkbutton(master, text="Key Up", variable=self.var_key_up).grid(
            row=1, column=1, sticky="w", padx=10
        )
        tk.Checkbutton(master, text="Key Name", variable=self.var_key_name).grid(
            row=1, column=2, sticky="w", padx=10
        )
        tk.Checkbutton(master, text="Scan Code", variable=self.var_scan_code).grid(
            row=1, column=3, sticky="w", padx=10
        )

        self.start_button = tk.Button(master, text="Start", command=self.start_logger)
        self.start_button.grid(row=1, column=4, padx=10)
        self.stop_button = tk.Button(
            master, text="Stop", state="disabled", command=self.stop_logger
        )
        self.stop_button.grid(row=1, column=5, padx=5)

        self.log_box = tk.Text(
            master, height=25, width=90, state="disabled", bg="#f0f0f0"
        )
        self.log_box.grid(row=2, column=0, columnspan=6, padx=10, pady=(10, 0))

        self.csv_label = tk.Label(
            master, text="", fg="blue", anchor="w", justify="left"
        )
        self.csv_label.grid(
            row=3, column=0, columnspan=6, sticky="w", padx=10, pady=(0, 10)
        )

        self.update_gui_log()

    def browse_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def update_gui_log(self):
        try:
            while True:
                msg = self.gui_queue.get_nowait()
                self.log_box.config(state="normal")
                self.log_box.insert(tk.END, msg + "\n")
                self.log_box.see(tk.END)
                self.log_box.config(state="disabled")
        except Empty:
            pass
        self.master.after(10, self.update_gui_log)

    def start_logger(self):
        if self.global_start_time is None:
            self.global_start_time = time.time()

        try:
            self.app = MainApp(
                output_dir=self.output_dir.get(),
                start_time=self.global_start_time,
                gui_queue=self.gui_queue,
            )
            self.app.record_key_down = self.var_key_down.get()
            self.app.record_key_up = self.var_key_up.get()
            self.app.record_key_name = self.var_key_name.get()
            self.app.record_scan_code = self.var_scan_code.get()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.logger_thread = Thread(target=self.app.run, daemon=True)
        self.logger_thread.start()

        self.csv_label.config(text=f"Fichier CSV : {self.app.filepath_csv}")

    def stop_logger(self):
        if self.app:
            self.app.stop()
            if self.logger_thread:
                self.logger_thread.join(timeout=2)

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")


def main():
    root = tk.Tk()
    gui = KeyloggerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
