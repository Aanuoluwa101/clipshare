from clipboard import Clipboard


class ServerInfo:
    def __init__(self):
        self.address = None
        self.name = None
        

if __name__ == "__main__":
    server_info = ServerInfo()
    print(server_info.clipboard.content)
    print(server_info.clipboard.state)
    server_info.clipboard.state = "failed"
    print(server_info.clipboard.state)