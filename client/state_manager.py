"""
Contains the `state_manager` function responsible for 
controlling the application flow based on the state.
"""

from utils import get_one_wifi_config
import threading
from client import client
from utils import get_base_ip


def state_manager(state):
    """
    Manages the application state and triggers actions accordingly.

    Parameters:
    - state (State): The state object for managing application data.
    """
    while True:
        if state.exit_signal.is_set():
            # if there is request to quit the entire app from the UI
            state.shutdown_signal.set()
            # state.server.is_running = False
            print("exiting state manager")
            break

        state.gateway = get_one_wifi_config("gateway")
        if state.gateway:
            state.client.base_ip = get_base_ip()
        if (
            state.gateway
            and not state.client.is_connected
            and not state.shutdown_signal.is_set()
            and state.connect_signal.is_set()
        ):
            # if there is wifi, the client is not connected, there is no disconnect
            # action from the UI and there is a connect action from the UI, start the client
            state.client.address = get_one_wifi_config("ip")

            print("starting client")
            client_thread = threading.Thread(target=client, args=(state,))
            client_thread.start()

        elif state.client.is_connected and (
            not state.gateway or state.shutdown_signal.is_set()
        ):
            # if the client is connected and there is a disconnect action from the UI
            # or wifi goes off, then stop the client
            state.shutdown_signal.set()
            state.client.is_connected = False


if __name__ == "__main__":
    exit_signal = threading.Event()
    state_manager(exit_signal)
