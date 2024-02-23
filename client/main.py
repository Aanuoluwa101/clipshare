"""Defines the entry point of the application"""

from ui.ui import start_ui
import time
import threading
from state_manager import state_manager
from state import State


if __name__ == "__main__":
    state = State()

    state_manager_thread = threading.Thread(target=state_manager, args=(state,))
    ui_thread = threading.Thread(target=start_ui, args=(state,))

    ui_thread.start()
    state_manager_thread.start()

    while True:
        if state.exit_signal.is_set():
            time.sleep(3)
            break
        continue
