import pyperclip

class Clipboard:
    NEW = "New"
    SENT = "Sent"
    RECEIVED = "Received"

    def __init__(self):
        self.__content = pyperclip.paste()
        self.local = self.__content
        self.send_state = Clipboard.NEW

    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, content):
        self.__content = content
        self.send_state = Clipboard.NEW
    
    def update_clipboard(self, new_content, send_state=None):
        self.__content = new_content
        self.send_state = Clipboard.NEW if not send_state else send_state


if __name__ == "__main__":
    clipboard = Clipboard()
    clipboard.update_clipboard("hello")
    print(clipboard.send_state)
