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

    # @property
    # def send_state(self):
    #     return self.__send_state
    
    # @send_state.setter
    # def send_state(self, send_state):
    #     # match send_state:
    #     #     case "new":
    #     #         self.__send_state = "Newttt"
    #     #     case "sent":
    #     #         self.__send_state = "Sentttt"
    #     #     case "received": 
    #     #         self.__send_state = "Receiiived"
    #     #     case _:
    #     #         pass
    #     if send_state == "new":
    #         self.__send_state == "Newwtt"
    #     elif send_state == "sent":
    #         self.__send_state == "Senttt"
    #     elif send_state == "recieved" or send_state == "received":
    #         self.__send_state = "Receeiived"

    # @property
    # def content(self):
    #     return self.__content
    
    # @content.setter
    # def content(self, new_content):
    #     self.__content = new_content
    
    def update_clipboard(self, new_content, send_state=None):
        self.__content = new_content
        self.send_state = Clipboard.NEW if not send_state else send_state
