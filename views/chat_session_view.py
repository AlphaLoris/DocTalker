import tkinter as tk
import tkinter.ttk as ttk

"""
class LaunchWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.launch_button = None
        self.org_entry = None
        self.org_label = None
        self.name_entry = None
        self.name_label = None
        self.email_entry = None
        self.email_label = None

        # User email
        self.email_label = tk.Label(self, text="Email Address:")
        self.email_label.pack(padx=20, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(padx=20, pady=5)

        # User name
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack(padx=20, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(padx=20, pady=5)

        # User organization
        self.org_label = tk.Label(self, text="Organization:")
        self.org_label.pack(padx=20, pady=5)
        self.org_entry = tk.Entry(self)
        self.org_entry.pack(padx=20, pady=5)

        # Initiate Chat Session Button
        self.launch_button = tk.Button(self, text="Initiate Chat Session", command=self.initiate_chat_session)
        self.launch_button.pack(padx=20, pady=10)

    # Define the behavior when the "Initiate Chat Session" button is clicked
    def initiate_chat_session(self):
        email = self.email_entry.get()
        name = self.name_entry.get()
        organization = self.org_entry.get()

        # Perform actions with the input data (such as initiating the chat session)
        # Here, I'm just printing the values to the console
        print(f"Email: {email}, Name: {name}, Organization: {organization}")
"""

class ChatSessionView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.chat_session_widgets = None
        self.chat_session_tab = None
        self.chat_session_notebook = None
        self.chat_session_controller = None
        self.chat_text_entry_text = None
        self.chat_history_textbox = None
        self.chat_session_window = None
        self.parent = parent

    def initiate_chat_session(self):

        # Create a Frame to hold Chat History Listbox and Scrollbar
        chat_history_frame = tk.Frame(self, bg="white")
        chat_history_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Add an empty Listbox to the frame
        self.chat_history_textbox = tk.Text(chat_history_frame, wrap=tk.WORD, bg="white")

        # Add Scrollbar to the frame
        chat_history_scrollbar = tk.Scrollbar(chat_history_frame)
        chat_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to listbox
        self.chat_history_textbox.config(yscrollcommand=chat_history_scrollbar.set)
        chat_history_scrollbar.config(command=self.chat_history_textbox.yview)

        self.chat_history_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

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

        # Configure rows and columns for resizing
        self.rowconfigure(0, weight=0)  # label row (weight = 0 means it won't expand)
        self.rowconfigure(1, weight=2)  # chat_history_frame row
        self.rowconfigure(2, weight=1)  # chat_text_entry_frame row
        self.columnconfigure(0, weight=1)  # all content in one column

        # Submit button
        submit_button_frame = tk.Frame(self)
        submit_button_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        submit_button = tk.Button(submit_button_frame, text="Submit", bg="white",
                                  command=self.on_submit)
        submit_button.pack(side=tk.RIGHT)

        # New session button
        new_session_button = tk.Button(submit_button_frame, text="New session", bg="white")
        new_session_button.pack(side=tk.LEFT)

    def set_chat_session_controller(self, controller):
        self.chat_session_controller = controller

    def add_tab(self, widget, tab_name):
        # Add the given widget as a new tab to the notebook
        self.chat_session_notebook.add(widget, text=tab_name)

    def on_submit(self):
        # Get the text from the Text widget
        chat_text = self.chat_text_entry_text.get("1.0", tk.END)
        # Clear the Text widget
        self.chat_text_entry_text.delete("1.0", tk.END)
        # Add the text to the Listbox
        self.chat_history_textbox.insert(tk.END, chat_text)
        self.chat_session_controller.submit_chat_text(chat_text)

