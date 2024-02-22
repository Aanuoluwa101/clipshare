""""Defines the Body class"""

import tkinter as tk


class Body:
    def __init__(self, root, send_clipboard):  
        """Initializes a Body instance
        
        Parameters:
        root (tk.Tk): the root element of the UI
        send_clipboard: callback function for the send button
        """ 
        self.error_message = tk.Label(root, font=('Helvetica', 9), fg="red", text="error")
        self.error_message.pack()
  
        body_frame = tk.Frame(root, width=300, height=200, padx=10, pady=30, background="#eeeeee")
        body_frame.pack()

        body_frame.pack_propagate(False)  


        self.clipboard = tk.Text(body_frame, width=35, height=10) 
        self.clipboard.grid(row=1, column=0, pady=10, padx=5, sticky="ew")

        button_label_frame = tk.Frame(body_frame, width=35)
        button_label_frame.grid(row=2, column=0, pady=5, padx=(5, 5), sticky="ew")

        self.send_button = tk.Button(button_label_frame, text="Send", command=send_clipboard, cursor="hand2", bg="#2c3e4c", padx=5, fg="white")
        self.send_button.pack(side="right", padx=(10, 0)) 

        self.clipboard_state = tk.Label(button_label_frame, font=('Helvetica', 9), padx=5, pady=3, bg="#2c3e4c", fg="white")
        self.clipboard_state.pack(side="left", padx=(0, 10))
