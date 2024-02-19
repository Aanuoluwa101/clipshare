from clipboard import Clipboard
from get_server_name import get_server_name

class ServerInfo:
    def __init__(self):
        self.is_running = False
        self.is_connected = False
        self.is_online = False
        self.address = None
        self.name = get_server_name()
        self.clipboard = Clipboard()
        self.passcode = None
    



if __name__ == "__main__":
    server_info = ServerInfo()
    print(server_info.clipboard.content)
    print(server_info.clipboard.state)
    server_info.clipboard.state = "failed"
    print(server_info.clipboard.state)