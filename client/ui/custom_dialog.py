"""Defines the CustomDialog class"""

import tkinter as tk
from tkinter import simpledialog


class CustomDialog(simpledialog.Dialog):
    def __init__(self, root, base_ip):
        """Initalizes a CustomDialog instance
        
        Parameters:
        root (tk.Tk): root element of the UI
        base_ip (str): base IP address
        """
        self.base_ip = base_ip
        super().__init__(root)

    def body(self, root):
        """Defines the body of the dialog box"""
        tk.Label(root, text="Server's IP:").grid(row=0)
        tk.Label(root, text="Passcode").grid(row=1)

        self.server_ip_entry = tk.Entry(root)
        self.passcode_entry = tk.Entry(root)

        self.server_ip_entry.insert(0, self.base_ip)
        self.server_ip_entry.grid(row=0, column=1)
        self.passcode_entry.grid(row=1, column=1)

        return self.server_ip_entry

    def apply(self):
        """Callback function for closing the dialog box"""
        server_ip = self.server_ip_entry.get()
        passcode = self.passcode_entry.get()

        self.result = (server_ip, passcode)


if __name__ == "__main__":
    root = tk.Tk()

    def connect_popup(root):
        dialog = CustomDialog(root, "hello")
        if not dialog.result:
            return
        server_ip, passcode = dialog.result

        # Now you can use the 'server_ip' and 'passcode' variables as needed
        if server_ip and passcode:
            # Do something with server_ip and passcode
            print(f"Server IP: {server_ip}, passcode: {passcode}")

    button = tk.Button(root, command=lambda: connect_popup(root), text="connect")
    button.pack()
    root.mainloop()
