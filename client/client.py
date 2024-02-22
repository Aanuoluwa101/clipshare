"""Defines the Client class, which represents the client-side functionality of the app
"""

import socket 
import pyperclip
import threading
from state import State
from clipboard import Clipboard


class Client:
    CONNECTED = "Connected"
    OK = "200"
    PORT = 12345

    def __init__(self, state):
        """initializes the Client instance

           Parameters:
           state (State): a State object (data store of the application)     
        """
        self.state = state
        
        if self.state.shutdown_signal.is_set():
            print("before socket creation")
            self.shutdown()
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = client_socket   
            print("socket created")
        except OSError:
            print("error creating socket")
            exit(1)

    def authenticate(self):
        """Authenticates the client with the server during the connection process"""
        #entered during connect
        print("authenticating")
        server_passcode = self.state.server.passcode
        client_name = self.state.client.name

        self.socket.send(server_passcode.encode('utf-8'))
        response = self.socket.recv(1024).decode('utf-8')
        if response == Client.OK:
            print(f"Authentication successful: {response}")
            print("sending name")
            self.socket.send(client_name.encode("utf-8"))
            response = self.socket.recv(1024).decode('utf-8')
            self.state.server.name = response 
            print(f"server name is {response}")
        else:
            self.state.error_message = "Authetication failed"
            self.shutdown()

    def connect(self):
        """Establishes a connection between the client and the server"""
        if self.state.shutdown_signal.is_set():
            self.shutdown()
        try:
            self.socket.settimeout(10)
            self.state.client.is_connecting = True
            self.socket.connect((self.state.server.address, Client.PORT))
            print("connected")
            #share names
            self.authenticate()

            self.state.client.is_connected = True
            self.state.error_message = ""
        except TimeoutError:
            print("connection timed out")
            self.state.error_message = "connection timed out"
            self.shutdown()
        except (ConnectionRefusedError, Exception) as e:
            self.state.error_message = "Unable to reach server! \n Ensure server is started and in same network with client"
            self.shutdown()
        finally:
            self.state.client.is_connecting = False
        

    def send_clipboard(self):
        """Sends the client's clipboard content to the server"""
        clipboard = self.state.client.clipboard.content
        self.socket.send(clipboard.encode('utf-8'))

        try:
            # response = self.socket.recv(1024).decode('utf-8')
            # if response == Client.OK:
            #     print(f"response from server: {response}")
            self.state.client.clipboard.update_clipboard(clipboard, Clipboard.SENT)
        except TimeoutError:
            self.state.error_message = "Operation timed out"
        except OSError:
            print("os error caught while sending clipboard")
            self.shutdown()
        finally:
            self.state.send_signal.clear()
        

    def receive_clipboard(self):
        """Receives the server's clipboard content"""
        try:
            server_clipboard = self.socket.recv(1024).decode('utf-8')
            if server_clipboard:
                self.state.client.clipboard.update_clipboard(server_clipboard, Clipboard.RECEIVED)
                pyperclip.copy(server_clipboard)
                print(f"successfully recieved: {server_clipboard}")
                #self.socket.send(Client.OK.encode('utf-8'))
            else:
                print("connection error, probably zero bytes sent")
                self.shutdown()
        except TimeoutError:
            return
        except OSError:
            print("os error caught while receiving clipboard")
            self.shutdown()
            #raise e
        
    def share_clipboard(self):
        """Continuously shares the clipboard content either by 
           sending or receiving based on the state of the send_signal"""
        self.socket.settimeout(2)
        while True:
            try:
                if self.state.send_signal.is_set():
                    self.send_clipboard()    
                else:
                    self.receive_clipboard()
                    
                if self.state.shutdown_signal.is_set():
                    self.shutdown()
            except ConnectionError:
                self.shutdown()
    
    def run(self):
        """Main method orchestrating the client's functionality"""
        if self.state.shutdown_signal.is_set():
            self.shutdown()
        try:
            # Connect to server
            self.connect()
            print("connected")
            self.state.client.is_connected = True 
            #share clipboard          
            self.share_clipboard()
        except ConnectionError:
            self.shutdown()
        except socket.error:
            print("socket error")
            self.shutdown()           
        except KeyboardInterrupt:
            #for testing purposes only
            self.shutdown()


    def shutdown(self):
        """Gracefully shuts down the client"""
        self.socket.close()
        self.state.shutdown_signal.clear()
        self.state.connect_signal.clear()
        self.state.client.is_connected = False
        print("shutting down gracefully")
        exit(0)


def client(state):
    """Function to be run by the state manager as the client thread"""
    state.connect_signal.clear()
    client = Client(state)
    client.run()

    


if __name__ == "__main__":
    from utils import get_one_wifi_config
    state = State()
    state.server.address = get_one_wifi_config("ip")

    send_signal = threading.Event()
    state.shutdown_signal = threading.Event()
    client(state)
