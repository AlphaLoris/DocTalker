import tkinter as tk


class ChatView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")  # Set the background color to white for better visibility

        # Add a simple label to the PromptsTab
        label = tk.Label(self, text="List of Prompts", bg="white")
        label.grid(pady=10, sticky='nsew')

        # Create a Frame to hold Chat History Listbox and Scrollbar
        chat_history_frame = tk.Frame(self, bg="white")
        chat_history_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Add an empty Listbox to the frame
        self.chat_history_listbox = tk.Listbox(chat_history_frame, bg="white")

        # Add Scrollbar to the frame
        chat_history_scrollbar = tk.Scrollbar(chat_history_frame)
        chat_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to listbox
        self.chat_history_listbox.config(yscrollcommand=chat_history_scrollbar.set)
        chat_history_scrollbar.config(command=self.chat_history_listbox.yview)

        self.chat_history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Text Entry Text Box
        # Create a Frame to hold Chat Text Entry Listbox and Scrollbar
        chat_text_entry_frame = tk.Frame(self, bg="white")
        chat_text_entry_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        # Create a Text widget in the frame
        self.chat_text_entry_text = tk.Text(chat_text_entry_frame, height=3, bg="white")

        # Add Scrollbar to the frame
        chat_text_entry_scrollbar = tk.Scrollbar(chat_text_entry_frame)
        chat_text_entry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to Text widget
        self.chat_text_entry_text.config(yscrollcommand=chat_text_entry_scrollbar.set)
        chat_text_entry_scrollbar.config(command=self.chat_text_entry_text.yview)

        # Pack the Text widget into the frame
        self.chat_text_entry_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.rowconfigure(0, weight=0)  # label row (weight = 0 means it won't expand)
        self.rowconfigure(1, weight=2)  # chat_history_frame row
        self.rowconfigure(2, weight=1)  # chat_text_entry_frame row

        self.columnconfigure(0, weight=1)  # all content in one column

        submit_button_frame = tk.Frame(self, bg="white")
        submit_button_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        submit_button = tk.Button(submit_button_frame, text="Submit", bg="white")
        submit_button.pack(side=tk.RIGHT)
