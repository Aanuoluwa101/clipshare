from server_info import ServerInfo
from client_info import ClientInfo
import threading 

class State:
    def __init__(self):
        self.server = ServerInfo()
        self.client = ClientInfo()
        self.__gateway = None
        self.error_message = ""

        self.shutdown_signal = threading.Event()
        self.connect_signal = threading.Event()
        self.send_signal = threading.Event()
        self.exit_signal = threading.Event()

    @property
    def gateway(self):
        return self.__gateway
    
    @gateway.setter
    def gateway(self, gateway):
        self.__gateway = gateway
        self.client.is_online = True if self.__gateway else False



if __name__ == "__main__":
    state = State()
    print(state.server.clipboard)
    print(state.client.clipboard)