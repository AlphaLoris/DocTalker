import tkinter as tk

# TODO: track cost of each chat session
# TODO: allow the admin to set a budget for each chat session
# TODO: track number of queries in each chat session
# TODO: track duration of each chat session

class ChatSessionsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")  # Set the background color to white for better visibility

        for col in range(12):
            self.columnconfigure(col, weight=1)

        # Configure rows if necessary
        for row in range(11):
            self.rowconfigure(row, weight=1)

        # Add a simple label to the PromptsTab
        self.label = tk.Label(self, text="Chat Sessions", bg="white")
        self.label.grid(row=0, column=5, rowspan=1, columnspan=2, padx=10, pady=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=1, column=0, rowspan=1, columnspan=12)

        # Add a "Launch Chat Session" button to the ChatSessionsTab
        self.launch_chat_session_button = tk.Button(self, text="Launch Chat Session", width=18,
                                                    command=self.controller.launch_chat_session)
        self.launch_chat_session_button.grid(row=1, column=5, padx=10, pady=10)
        self.end_chat_session_button = tk.Button(self, text="End Chat Session", width=18)
        self.end_chat_session_button.grid(row=1, column=6, padx=10, pady=10)

        # Add an empty Listbox to the ChatSessionsTab
        self.chat_sessions_listbox = tk.Listbox(self, bg="white")
        self.chat_sessions_listbox.grid(row=2, column=0, columnspan=12, rowspan=9, padx=10, pady=10, sticky='nsew')

