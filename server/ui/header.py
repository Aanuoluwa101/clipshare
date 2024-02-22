"""Defines the Header class"""

import tkinter as tk

class Header:
    def __init__(self, root, show_server_details):
        """Initializes a Header instance
        
        root (tk.TK): the root element of the UI
        show_server_details: callback function for the server name button
        """
        header_frame = tk.Frame(root, bg="#2c3e4c", padx=3, pady=5)
        header_frame.pack(fill=tk.X)

        self.server_name = tk.Button(header_frame, font=('Helvetica', 9), command=show_server_details, cursor="hand2", background="#eeeeee", fg="black")
        self.server_name.pack(side="left", padx=(3, 0)) 