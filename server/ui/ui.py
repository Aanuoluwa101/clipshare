from tkinter import *
from tkinter import ttk
import tkinter as tk
import pyperclip
import time
from .header import Header
from .body import Body
from .footer import Footer
from .server_details import ServerDetails


CONNECTED = "Connected"
AWAITING = "Awaiting Connections..."
OFFLINE = "Offline"


class UI:
    def __init__(self, state):
        self.state = state
        self.root = Tk()
        self.root.title("Clipshare-Server")
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=350, height=350)
        self.root.configure(background="#eeeeee")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.header = Header(self.root, self.show_server_details)
        self.body = Body(self.root, self.send_clipboard)
        self.footer = Footer(self.root)

        self.showing_server_details = False

        self.error_msg_update_count = 0

    def start(self):
        self.update()
        self.root.mainloop()

    def update(self):
        try:
            # Header
            # server_name
            self.header.server_name.config(text=self.state.server.name)

            # Body
            # error message
            self.body.error_message.config(text=self.state.error_message)
            # print(self.state.error_message)
            if self.error_msg_update_count == 3:
                self.error_msg_update_count = 0
                self.state.error_message = ""
            self.error_msg_update_count += 1

            # clipboard
            clipboard = pyperclip.paste()
            if (
                clipboard != self.state.server.clipboard.local
                and clipboard != self.state.server.clipboard.content
            ):
                self.state.server.clipboard.update_clipboard(clipboard)
                self.state.server.clipboard.local = clipboard
            self.body.clipboard.delete("1.0", tk.END)
            self.body.clipboard.insert("1.0", self.state.server.clipboard.content)

            # clipboard state
            self.body.clipboard_state.config(
                text=self.state.server.clipboard.send_state
            )

            # Footer
            # gateway (wifi)
            self.footer.gateway.config(text=f"Wifi {self.state.gateway}")

            # server state
            # we probably need to acquire a lock here
            if not self.state.server.is_online:
                server_state = "Offline"
            elif self.state.server.is_running and self.state.server.is_connected:
                server_state = "Running, Connected"
            elif self.state.server.is_running and not self.state.server.is_connected:
                server_state = "Running, Awaiting connections..."
            elif not self.state.server.is_running and self.state.server.is_online:
                server_state = "Server Error"

            self.footer.server_state.config(text=server_state)

        except Exception as e:
            print(e)
            pass
            # run itself again after 1000 m
        finally:
            # print("update")
            self.root.after(500, self.update)

    def on_close(self):
        self.state.exit_signal.set()
        self.root.destroy()
        time.sleep(3)

    def send_clipboard(self):
        # if self.state.server.clipboard.send_state == "New" and self.state.server.is_connected:
        if self.state.server.is_connected:
            self.state.send_signal.set()
        elif self.state.server.is_online and not self.state.server.is_connected:
            self.state.error_message = "Cannot send! Not Connected"
        elif not self.state.server.is_online:
            print("cannot send clipboard now")
            self.state.error_message = "Offline. Connect to a wifi"

    def show_server_details(self):
        def on_server_details_close():
            self.showing_server_details = False
            server_details.destroy()

        # if self.state.server.is_online and not self.state.server.is_connected and not self.showing_server_details:
        if self.state.server.is_online and not self.showing_server_details:
            self.showing_server_details = True
            name, address, passcode = (
                self.state.server.name,
                self.state.server.address,
                self.state.server.passcode,
            )

            server_details = ServerDetails(
                self.root, name, address, passcode, on_server_details_close
            )
        elif not self.state.server.is_online:
            self.state.error_message = "Offline! Connect to a wifi"
        # elif self.state.server.is_connected:
        #     self.state.error_message = "Cannot show details while connected"


def start_ui(state):
    """Function to be run by the state manager as the UI thread"""
    ui = UI(state)
    ui.start()
