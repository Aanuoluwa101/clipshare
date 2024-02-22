"""
Defines the State class which encapsulates all application data
"""

from server_info import ServerInfo
from client_info import ClientInfo
import threading

class State:
    def __init__(self):
        """Instantiates a State object"""
        self.server = ServerInfo()
        self.client = ClientInfo()
        self.__gateway = None
        self.error_message = ""

        self.shutdown_signal = threading.Event()
        self.send_signal = threading.Event()
        self.exit_signal = threading.Event()

    @property
    def gateway(self):
        """Retrieves the gateway (wifi) ip of the app"""
        return self.__gateway
    
    @gateway.setter
    def gateway(self, gateway):
        """Updates the gateway (wifi) ip of the app"""
        self.__gateway = gateway
        self.server.is_online = True if self.__gateway else False


if __name__ == "__main__":
    state = State()
    print(state.server.clipboard)
    print(state.client.clipboard)