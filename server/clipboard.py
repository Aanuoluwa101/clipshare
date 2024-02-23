"""Defines the Clipboard class"""

import pyperclip


class Clipboard:
    NEW = "New"
    SENT = "Sent"
    RECEIVED = "Received"

    def __init__(self):
        """Initializes the Clipboard instance"""
        self.__content = pyperclip.paste()
        self.local = self.__content
        self.send_state = Clipboard.NEW

    @property
    def content(self):
        """Retrieves the current content of the clipboard"""
        return self.__content

    # @content.setter
    # def content(self, content):
    #     self.__content = content
    #     self.send_state = Clipboard.NEW

    def update_clipboard(self, new_content, send_state=None):
        """Updates the content of the clipboard and its send state

        Parameters:
        new_content (str): new clipboard content
        send_state (str): state of the clipboard. NEW, SENT or RECEIVED
        """
        self.__content = new_content
        self.send_state = Clipboard.NEW if not send_state else send_state
