"""
Defines the ClientInfo class which encapsulates client information
"""

import pyperclip


class ClientInfo:
    def __init__(self):
        """Instantiate a ClientI object"""
        self.address = None
        self.name = None


if __name__ == "__main__":
    client_info = ClientInfo()
    print(client_info.clipboard)
