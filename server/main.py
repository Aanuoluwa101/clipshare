"""Defines the entry point of the application"""

from ui.ui import start_ui
import time
import threading
from state_manager import state_manager
from state import State
import os


if __name__ == "__main__":
    lock = "lock_file"
    if os.path.exists(lock):
        print("Only one instance of program is allowed to run")
        exit(1)

    with open(lock, "w") as file:
        file.write(str(os.getpid()))

    state = State()

    state_manager_thread = threading.Thread(target=state_manager, args=(state,))
    ui_thread = threading.Thread(target=start_ui, args=(state,))

    ui_thread.start()
    state_manager_thread.start()

    while True:
        if state.exit_signal.is_set():
            time.sleep(3)
            os.remove(lock)
            break
        continue
