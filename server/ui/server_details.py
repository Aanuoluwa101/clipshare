"""Defines the ServerDetails class which is a popup 
   that shows server details
"""

import tkinter as tk
from tkinter import ttk

class ServerDetails():
    def __init__(self, root, name, address, passcode, on_close):
        """Initializes a ServerDetails instance
           
        Parameters:
        root (tk.Tk): root element of the UI
        name (str): name of the server
        address (str): IP address of the server
        passcode (str): passcode of the server
        on_close: a callback function for closing the popup
        """
        self.server_details = tk.Toplevel(root)
        self.server_details.title(name)
        self.server_details.configure(background="#2c3e4c")
        self.server_details.protocol("WM_DELETE_WINDOW", on_close)
        self.server_details.resizable(width=False, height=False)

        root_x = root.winfo_x()
        root_y = root.winfo_y()
        width = self.server_details.winfo_reqwidth()
        height = self.server_details.winfo_reqheight()
        x = root_x + (root.winfo_width() // 2) - (width // 2)
        y = root_y + (root.winfo_height() // 2) - (height // 2)

        # Set the geometry to center the popup relative to the root UI
        self.server_details.geometry(f"+{x}+{y}")

        # Add labels to the Toplevel window
        server_address = ttk.Label(self.server_details, text=f"Address:    {address}", background="#2c3e4c", font=("Helvetica", 9, "bold"), foreground="white")
        server_address.grid(row=0, padx=10, pady=10)

        server_passcode = ttk.Label(self.server_details, text=f"Passcode:  {passcode}", background="#2c3e4c", font=("Helvetica", 9, "bold"), foreground="white")
        server_passcode.grid(row=1, sticky="w", padx=10, pady=10)

    def destroy(self):
        """Closes the popup"""
        self.server_details.destroy()