import tkinter as tk
from tkinter import filedialog


class DocumentsView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        self.configure(bg="white")  # Set the background color to white for better visibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create a frame for source directory elements
        self.source_dir_frame = tk.Frame(self, bg="white")
        self.source_dir_frame.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Add elements to the frame instead of the main widget
        self.source_dir_label = tk.Label(self.source_dir_frame, text="Document Source Directory", bg="white")
        self.source_dir_label.grid(row=0, column=0, padx=5, columnspan=2, sticky="w")

        self.source_dir = tk.StringVar()
        self.source_dir_entry = tk.Entry(self.source_dir_frame, textvariable=self.source_dir, width=50)
        self.source_dir_entry.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        self.source_dir_button = tk.Button(self.source_dir_frame, text="Source Directory",
                                           command=self.select_source_dir)
        self.source_dir_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.load_files_button = tk.Button(self, text="Load Files", command=self.load_files)
        self.load_files_button.grid(row=2, column=0, padx=10, sticky="w")

        # Add a blank row
        blank_label = tk.Label(self, text="", bg="white")
        blank_label.grid(row=3, column=0)

        # Add a documents Listbox to the PromptsTab
        listbox_label = tk.Label(self, text="List of Documents", bg="white")
        listbox_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.documents_listbox = tk.Listbox(self, bg="white")
        self.documents_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew", ipady=50)

    def set_controller(self, documents_controller):
        self.controller = documents_controller

    def select_source_dir(self):
        """Open file dialog to select source directory"""
        source_dir = filedialog.askdirectory()
        self.source_dir.set(source_dir)
        print("Selected source directory:", source_dir)

    def load_files(self):
        """Load files from source directory"""
        source_dir = self.source_dir.get()
        print("Loading files from source directory:", source_dir)
        self.controller.load_files(source_dir)

    def populate_listbox(self, filenames):
        for file in filenames:
            self.documents_listbox.insert(tk.END, file)

    def get_selected_files(self):
        return [self.documents_listbox.get(i) for i in self.documents_listbox.curselection()]

