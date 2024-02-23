import socket
import pyperclip
from state import State
from utils import generate_passcode
from clipboard import Clipboard


class Server:
    CONNECTED = "Connected"
    AWAITING = "Awaiting Connections"
    STOPPED = "Stopped"
    OK = "200"
    PORT = 12345

    def __init__(self, state):
        self.state = state
        if self.state.shutdown_signal.is_set():
            print("before socket creation")
            self.state.shutdown_signal.clear()
            self.shutdown()

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.state.server.address, Server.PORT))
            server_socket.listen(1)
            # server_socket.setblocking(False)
            # server_socket.settimeout(2)
            self.socket = server_socket

        except OSError as e:
            print("error creating socket")
            exit(1)

    def authenticate(self):
        # entered during connect
        server_passcode = self.state.server.passcode
        server_name = self.state.server.name
        print("authenticating")
        try:
            passcode = self.client_socket.recv(1024).decode("utf-8")
            if passcode == server_passcode:
                self.client_socket.send(Server.OK.encode("utf-8"))
                print(f"Client successfully authenticated")
                client_name = self.client_socket.recv(1024).decode("utf-8")
                if client_name:
                    print(f"client name is {client_name}")
                    print("sending server name")
                    self.client_socket.send(server_name.encode("utf-8"))
                    return True
                else:
                    print("error sending name")
                    self.client_socket.close()
                    return False
            else:
                # self.state.error_message = "Authetication failed"
                print("authentication failed")
                self.client_socket.close()
                return False
        except TimeoutError:
            print("authentication failed")
            self.client_socket.close()
            return False

    # def share_names(self):
    #     self.state.client.name = self.client_socket.recv(1024).decode('utf-8')
    #     self.client_socket.send(Server.OK.encode('utf-8'))
    #     print(f"client name is: {self.state.client.name}")

    def connect(self):
        self.socket.settimeout(5)
        while True:
            try:
                # what are the things returned by socket.accept...can we extend it?
                client_socket, client_address = self.socket.accept()
                client_socket.settimeout(5)
                self.client_socket = client_socket
                is_autheticated = self.authenticate()
                if not is_autheticated:
                    raise ConnectionError
                self.state.server.is_connected = True
            except TimeoutError:
                if self.state.shutdown_signal.is_set():
                    self.state.shutdown_signal.clear()
                    self.shutdown()
                else:
                    continue

            # client_info.connect()
            # print(f"server state in connect method: {state.server.is_running}")
            return client_address
        # shouldn't we check different connection errors here? and raise them

    def send_clipboard(self):
        clipboard = self.state.server.clipboard.content
        try:
            self.client_socket.send(clipboard.encode("utf-8"))
            print("sending clipboard")

            # response = self.client_socket.recv(1024).decode('utf-8')
            # if response == Server.OK:
            #     print(f"response from client: {response}")
            self.state.server.clipboard.update_clipboard(clipboard, Clipboard.SENT)
        except TimeoutError:
            #######
            self.state.error_message = "Operation timed out"
        self.state.send_signal.clear()

    def recieve_clipboard(self):
        try:
            # print("receiving clipboard")
            client_clipboard = self.client_socket.recv(1024).decode("utf-8")
            # print("checking condition")
            if client_clipboard:
                # self.client_socket.send(Server.OK.encode('utf-8'))
                # pyperclip.copy(client_clipboard) #THIS IS VALID....
                self.state.server.clipboard.update_clipboard(
                    client_clipboard, Clipboard.RECEIVED
                )
                pyperclip.copy(client_clipboard)
                # print("successfully recieved")
            else:
                self.client_socket.close()
                # print("client no longer connected")
                raise ConnectionError
        except TimeoutError:
            return
        except OSError as e:
            raise e

    def share_clipboard(self):
        while True:
            try:
                if self.state.send_signal.is_set():
                    self.send_clipboard()
                # Receive
                else:
                    self.recieve_clipboard()

                if self.state.shutdown_signal.is_set():
                    self.state.shutdown_signal.clear()
                    self.shutdown()
            except ConnectionError:
                # print('caught a connection error')
                self.state.server.is_connected = False
                self.client_socket.close()
                raise ConnectionError

    def run(self):
        while True:
            if self.state.shutdown_signal.is_set():
                self.state.shutdown_signal.clear()
                self.shutdown()
            try:
                self.state.server.is_running = True
                self.state.server.passcode = generate_passcode()
                print("awaiting connections...")
                # set connection_state to awaiting connections

                # Connect to client
                self.state.client.address = self.connect()
                # catch connection errors and continue
                print("connected")
                # state.server.is_connected = True
                # state.client.is_connected = True
                # print(f"Accepted connection from {self.client_address}")
                # set variable to connected
                # print("sharing data")
                self.share_clipboard()
            except ConnectionError:
                # set client state to disconnected and server state to awaiting connections
                # print("client closed connection")
                continue

            # what's the difference between socket error and connection error
            except socket.error as e:
                # the possible socket errors will determine what we will set the variables to.
                # client definitely becomes disconnected
                print("socket error")
                # state.server.is_running = False
                # state.server.is_connected = False
                self.shutdown()
                exit(1)

            # we are leaving keyboard interrupt only for testing purposes
            except KeyboardInterrupt:
                self.shutdown()

    def shutdown(self):
        try:
            self.client_socket.close()
            self.server_socket.close()
        except Exception:
            pass
        finally:
            self.state.server.is_running = False
            self.state.server.is_connected = False
            print("shutting down gracefully")
            exit(0)


def server(state):
    server = Server(state)
    # print(f"server state inside server: {state.server.is_running}")
    server.run()

    # print("calling the run function")


if __name__ == "__main__":
    # we must have a way of passing client state and name around...shared global variable
    state = State()
    state.server.address = "192.168.1.152"
    server(state)

    # it's not reflecting the recieved
    # it's not detecting connection close
