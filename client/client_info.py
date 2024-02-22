"""
Defines the ClientInfo class which encapsulates client information
"""


from clipboard import Clipboard
from utils import get_client_name


class ClientInfo:
    def __init__(self):
        """Instantiate a ClientInfo object"""
        self.is_connected = False
        self.is_connecting = False
        self.is_online = False
        self.address = None
        self.clipboard = Clipboard()
        self.name = get_client_name()
        self.base_ip = None

   
if __name__ == "__main__":
    client_info = ClientInfo()
    print(client_info.clipboard)