import tkinter as tk


class ChatSessionsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")  # Set the background color to white for better visibility

        # Add a simple label to the PromptsTab
        label = tk.Label(self, text="Chat Sessions", bg="white")
        label.pack(pady=10)

        # Add an empty Listbox to the ChatSessionsTab
        chat_sessions_listbox = tk.Listbox(self, bg="white")
        chat_sessions_listbox.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)