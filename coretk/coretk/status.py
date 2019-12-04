"status bar"
import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.status = None
        self.statusvar = tk.StringVar()
        self.progress_bar = None
        self.zoom = None
        self.cpu_usage = None
        self.memory = None
        self.emulation_light = None
        self.running = False
        self.draw()

    def draw(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.progress_bar = ttk.Progressbar(
            self, orient="horizontal", mode="indeterminate"
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")

        self.status = ttk.Label(self, textvariable=self.statusvar, anchor=tk.CENTER)
        self.statusvar.set("status")
        self.status.grid(row=0, column=1, sticky="ew")

        self.zoom = ttk.Label(self, text="zoom", anchor=tk.CENTER)
        self.zoom.grid(row=0, column=2, sticky="ew")

        self.cpu_usage = ttk.Label(self, text="cpu usage", anchor=tk.CENTER)
        self.cpu_usage.grid(row=0, column=3, sticky="ew")

        self.emulation_light = ttk.Label(self, text="emulation light", anchor=tk.CENTER)
        self.emulation_light.grid(row=0, column=4, sticky="ew")

    def start_session_callback(self, process_time):
        num_nodes = len(self.app.core.canvas_nodes)
        num_links = len(self.app.core.links)
        self.progress_bar.stop()
        self.statusvar.set(
            "Network topology instantiated in %s seconds (%s node(s) and %s link(s))"
            % ("%.3f" % process_time, num_nodes, num_links)
        )

    def stop_session_callback(self, cleanup_time):
        self.progress_bar.stop()
        self.statusvar.set("Cleanup completed in %s seconds" % "%.3f" % cleanup_time)