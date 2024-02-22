"""
Defines the ServerInfo class which encapsulates server information
"""


class ServerInfo:
    def __init__(self):
        """Instantiates a ServerInfo object"""
        self.address = None
        self.name = None
        

if __name__ == "__main__":
    server_info = ServerInfo()
    print(server_info.clipboard.content)
    print(server_info.clipboard.state)
    server_info.clipboard.state = "failed"
    print(server_info.clipboard.state)