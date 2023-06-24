import tkinter as tk


class ChatSessionView:
    def __init__(self, parent, controller):
        self.controller = controller

        # Create a new Toplevel window for the chat session
        self.window = tk.Toplevel(parent)

        # Optionally set the title of the new window
        self.window.title("Chat Session")

        # Create a Frame to hold Chat History Listbox and Scrollbar
        chat_history_frame = tk.Frame(self.window, bg="blue")
        chat_history_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Add an empty Listbox to the frame
        self.chat_history_listbox = tk.Listbox(chat_history_frame, bg="blue")

        # Add Scrollbar to the frame
        chat_history_scrollbar = tk.Scrollbar(chat_history_frame)
        chat_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to listbox
        self.chat_history_listbox.config(yscrollcommand=chat_history_scrollbar.set)
        chat_history_scrollbar.config(command=self.chat_history_listbox.yview)

        self.chat_history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Text Entry Text Box
        # Create a Frame to hold Chat Text Entry Listbox and Scrollbar
        chat_text_entry_frame = tk.Frame(self.window, bg="green")
        chat_text_entry_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        # Create a Text widget in the frame
        self.chat_text_entry_text = tk.Text(chat_text_entry_frame, height=3, bg="green")

        # Add Scrollbar to the frame
        chat_text_entry_scrollbar = tk.Scrollbar(chat_text_entry_frame)
        chat_text_entry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to Text widget
        self.chat_text_entry_text.config(yscrollcommand=chat_text_entry_scrollbar.set)
        chat_text_entry_scrollbar.config(command=self.chat_text_entry_text.yview)

        # Pack the Text widget into the frame
        self.chat_text_entry_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Configure rows and columns for resizing
        self.window.rowconfigure(0, weight=0)  # label row (weight = 0 means it won't expand)
        self.window.rowconfigure(1, weight=2)  # chat_history_frame row
        self.window.rowconfigure(2, weight=1)  # chat_text_entry_frame row
        self.window.columnconfigure(0, weight=1)  # all content in one column

        # Submit button
        submit_button_frame = tk.Frame(self.window)
        submit_button_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        submit_button = tk.Button(submit_button_frame, text="Submit", bg="white",
                                  command=self.controller.submit_chat_text)
        submit_button.pack(side=tk.RIGHT)

        # New session button
        new_session_button = tk.Button(submit_button_frame, text="New session", bg="white")
        new_session_button.pack(side=tk.LEFT)