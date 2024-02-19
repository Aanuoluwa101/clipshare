from ipconfig import get_wifi_config_details
import threading
from client import client
from get_base_ip import get_base_ip

def state_manager(state):
    while True: 
        if state.exit_signal.is_set():
            state.shutdown_signal.set()
            state.server.is_running = False
            print("exiting state manager")
            break

        state.gateway = get_wifi_config_details("gateway")
        if state.gateway:
            state.client.base_ip = get_base_ip()
        if state.gateway and not state.client.is_connected and not state.shutdown_signal.is_set() and state.connect_signal.is_set():      #if there is wifi and server is not running
            state.client.address = get_wifi_config_details("ip")

            print("starting client")
            client_thread = threading.Thread(target=client, args=(state,))
            client_thread.start()
 
        elif state.client.is_connected and (not state.gateway or state.shutdown_signal.is_set()):   #no wifi and there is a running server? Kill it.
            state.shutdown_signal.set()
            state.client.is_connected = False
    
if __name__ == "__main__":
    exit_signal = threading.Event()       
    state_manager(exit_signal)