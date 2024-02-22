from utils import get_one_wifi_config
import threading
from server import server

def state_manager(state):
    while True: 
        if state.exit_signal.is_set():
            state.shutdown_signal.set()
            state.server.is_running = False
            print("exiting state manager")
            break

        state.gateway = get_one_wifi_config("gateway")
        #if there is wifi and server is not running, start it
        if state.gateway and not state.server.is_running:      
            state.server.address = get_one_wifi_config("ip")
            print("starting server")
            server_thread = threading.Thread(target=server, args=(state,))
            server_thread.start()
 
        #no wifi and there is a running server? Kill it.
        elif not state.gateway and state.server.is_running:
            state.shutdown_signal.set()
            state.server.is_running = False
            state.client.is_connected = False
    
if __name__ == "__main__":
    exit_signal = threading.Event()       
    state_manager(exit_signal)