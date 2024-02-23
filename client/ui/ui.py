"""Defines the UI class"""

from tkinter import *
import tkinter as tk
import pyperclip
import time
from .header import Header
from .body import Body
from .footer import Footer
from .is_valid_ip import is_valid_ip
from .custom_dialog import CustomDialog


CONNECTED = "Online, Connected"
DISCONNECTED = "Online, Not Connected"
OFFLINE = "Offline"

DISCONNECT = "Disconnect"
CONNECTING = "Connecting..."
CONNECT = "Connect"


class UI:
    def __init__(self, state):
        """Initializes a UI instance

        Parameters:
        state (State): a state instance containing app data
        """
        self.state = state
        self.root = Tk()
        self.root.title("Clipshare-Client")
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=350, height=350)
        self.root.configure(background="#eeeeee")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.header = Header(self.root, self.connect)
        self.body = Body(self.root, self.send_clipboard)
        self.footer = Footer(self.root)

        self.error_msg_update_count = 0

    def update(self):
        """Updates all components of the UI with the app's current state"""
        try:
            # HEADER
            # client name
            self.header.client_name.config(text=self.state.client.name)

            # connect button
            if self.state.client.is_connected:
                connect_button_text = DISCONNECT
            elif self.state.client.is_connecting and not self.state.client.is_connected:
                connect_button_text = CONNECTING
            else:
                connect_button_text = CONNECT
            self.header.connect_button.config(text=connect_button_text)

            # BODY
            # error message
            self.body.error_message.config(text=self.state.error_message)
            if self.error_msg_update_count == 5:
                self.error_msg_update_count = 0
                self.state.error_message = ""
            self.error_msg_update_count += 1

            # clipboard
            clipboard = pyperclip.paste()
            if (
                clipboard != self.state.client.clipboard.local
                and clipboard != self.state.client.clipboard.content
            ):
                self.state.client.clipboard.update_clipboard(clipboard)
                self.state.client.clipboard.local = clipboard

            self.body.clipboard.delete("1.0", tk.END)
            self.body.clipboard.insert("1.0", self.state.client.clipboard.content)

            # clipboard_state
            self.body.clipboard_state.config(
                text=self.state.client.clipboard.send_state
            )

            # FOOTER
            # gateway (wifi)
            self.footer.gateway.config(text=f"Wifi {self.state.gateway}")

            # client state
            if not self.state.client.is_online:
                client_state = OFFLINE
            elif self.state.client.is_connected:
                client_state = CONNECTED
            elif not self.state.client.is_connected:
                client_state = DISCONNECTED
            self.footer.client_state.config(text=client_state)

        except Exception as e:
            print(e)
            pass
        finally:
            self.root.after(500, self.update)

    def on_close(self):
        """Callback function for closing the UI"""
        self.state.exit_signal.set()
        self.root.destroy()
        time.sleep(3)

    def send_clipboard(self):
        """Callback function for sending the clipboard"""
        if self.state.client.is_connected:
            self.state.send_signal.set()
        elif self.state.client.is_online and not self.state.client.is_connected:
            self.state.error_message = "Cannot send! Not Connected"
        elif not self.state.client.is_online:
            print("cannot send clipboard now")
            self.state.error_message = "Offline. Connect to a wifi"

    def connect(self):
        """Callback function for connecting to the server"""
        if not self.state.client.is_connected and self.state.client.is_online:
            result = self.connect_popup(self.state.client.base_ip)
            if not result:
                return
            elif not is_valid_ip(result[0]):
                self.state.error_message = "Invalid IP"
            elif not result[1]:
                self.state.error_message = "Enter a valid passcode"

            else:
                if self.state.client.is_online:
                    self.state.server.address = result[0]
                    self.state.server.passcode = result[1]
                    self.state.connect_signal.set()
                else:
                    print("client is offline")
        elif not self.state.client.is_online:
            self.state.error_message = "Offline. Connect to a wifi"
        else:
            self.state.shutdown_signal.set()

    def connect_popup(self, base_ip):
        """Creates a custom connect dialog box

        Parameters:
        base_ip (str): the base IP address
        """
        dialog_box = CustomDialog(self.root, base_ip)
        return dialog_box.result

    def start(self):
        """Starts the UI"""
        self.update()
        self.root.mainloop()


def start_ui(state):
    """Function to be run by the state manager as the UI thread"""
    ui = UI(state)
    ui.start()
