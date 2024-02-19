import tkinter as tk

class Footer:
    def __init__(self, root):
        footer_frame = tk.Frame(root, bg="#2c3e4c", padx=3, pady=2)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, anchor=tk.S)

        self.server_state = tk.Label(footer_frame, font=('Helvetica', 8), bg="#2c3e4c", fg="white")
        self.server_state.pack(side="right")

        self.gateway = tk.Label(footer_frame, font=('Helvetica', 8), bg="#2c3e4c", fg="white")
        self.gateway.pack(side="left")
