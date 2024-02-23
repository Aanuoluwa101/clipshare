"""Defines the Header class"""

import tkinter as tk


class Header:
    def __init__(self, root, connect):
        """Initializes a Header instance

        root (tk.TK): the root element of the UI
        connect: callback function for the connect button
        """
        header_frame = tk.Frame(root, bg="#2c3e4c", padx=3, pady=5)
        header_frame.pack(fill=tk.X)

        self.client_name = tk.Button(
            header_frame, font=("Helvetica", 9), background="#eeeeee", fg="black"
        )
        self.client_name.pack(
            side="left", padx=(3, 0)
        )  # Adds padding to the right of the button

        self.connect_button = tk.Button(
            header_frame,
            font=("Helvetica", 9),
            command=connect,
            cursor="hand2",
            background="#eeeeee",
            fg="black",
        )
        self.connect_button.pack(side="right", padx=(0, 3))
