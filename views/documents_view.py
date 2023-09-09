import tkinter as tk
from tkinter import filedialog


class DocumentsView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        self.configure(bg="white")  # Set the background color to white for better visibility

        # Add a simple label to the PromptsTab
        label = tk.Label(self, text="List of Documents", bg="white")
        label.pack(pady=10)

        # Add a source directory Entry and Button to the PromptsTab
        self.source_dir = tk.StringVar()
        self.source_dir_entry = tk.Entry(self, textvariable=self.source_dir, width=50)
        self.source_dir_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.source_dir_button = tk.Button(self, text="Source Directory",
                                           command=self.select_source_dir)
        self.source_dir_button.grid(row=0, column=1, padx=10, sticky="w")  # Same row as the Entry, next column

        # Load Files Button
        self.load_files_button = tk.Button(self, text="Test",
                                           command=self.load_files)
        self.load_files_button.grid(row=3, columnspan=2, padx=10, pady=10, sticky="w")

        # Add an empty Listbox to the PromptsTab
        self.documents_listbox = tk.Listbox(self, bg="white")
        self. documents_listbox.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

    def set_controller(self, documents_controller):
        self.controller = documents_controller

    def select_source_dir(self):
        """Open file dialog to select source directory"""
        source_dir = filedialog.askdirectory()
        self.source_dir.set(source_dir)
        print("Selected source directory:", source_dir)

    def load_files(self):
        """Load files from source directory"""
        self.controller.load_files()
