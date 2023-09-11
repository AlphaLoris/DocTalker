import tkinter as tk
from tkinter import filedialog
from utils.log_config import setup_colored_logging
import logging

# Setup colored logging and initialize logger
setup_colored_logging()
logger = logging.getLogger(__name__)


class DocumentsView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        logger.debug("Initializing DocumentsView.")
        self.h_scroll = None
        self.v_scroll = None
        self.controller = None

        self.configure(bg="white")  # Set the background color to white for better visibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create a frame for source directory elements
        self.source_dir_frame = tk.Frame(self, bg="white")
        self.source_dir_frame.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Elements within source_dir_frame
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
        blank_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Frame for the Listbox and its scrollbars
        self.listbox_frame = tk.Frame(self, bg="white")
        self.listbox_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.listbox_frame.grid_columnconfigure(0, weight=1)
        self.listbox_frame.grid_rowconfigure(0, weight=1)

        # Initialize the scrollbars first
        self.v_scroll = tk.Scrollbar(self.listbox_frame, orient="vertical")
        self.h_scroll = tk.Scrollbar(self.listbox_frame, orient="horizontal")

        # Elements within listbox_frame
        self.listbox_label = tk.Label(self.listbox_frame, text="Indexed Documents", bg="white")
        self.listbox_label.grid(row=0, column=0, columnspan=1, sticky="w")

        self.documents_listbox = tk.Listbox(self.listbox_frame, bg="white", yscrollcommand=self.v_scroll.set,
                                            xscrollcommand=self.h_scroll.set, selectmode=tk.MULTIPLE)
        self.documents_listbox.grid(row=1, column=0, sticky="nsew")

        self.v_scroll.config(command=self.documents_listbox.yview)
        self.v_scroll.grid(row=1, column=1, sticky="ns")

        self.h_scroll.config(command=self.documents_listbox.xview)
        self.h_scroll.grid(row=2, column=0, sticky="ew")

        # Corner frame to make the scrollbars look continuous
        corner_frame = tk.Frame(self.listbox_frame, bg=self.v_scroll.cget("bg"), width=17, height=17)
        corner_frame.grid(row=2, column=1, sticky="ne")

        # Button to remove selected files
        self.remove_files_button = tk.Button(self.listbox_frame, text="Remove Files",
                                             command=self.remove_selected_files)
        self.remove_files_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

    def set_controller(self, documents_controller):
        self.controller = documents_controller
        logger.debug("Controller set for DocumentsView.")

    def select_source_dir(self):
        """Open file dialog to select source directory"""
        source_dir = filedialog.askdirectory()
        if not source_dir:
            logger.warning("No source directory selected.")
            return
        self.source_dir.set(source_dir)
        logger.info(f"Selected source directory: {source_dir}")

    def load_files(self):
        """Load files from source directory"""
        source_dir = self.source_dir.get()
        if not source_dir:
            logger.warning("Attempted to load files without selecting a source directory.")
            return
        logger.info(f"Loading files from source directory: {source_dir}")
        loaded_files = self.controller.load_files(source_dir)  # Assuming this returns a list of loaded files
        self.controller.add_files(loaded_files)
        self.populate_listbox(loaded_files)

    def remove_selected_files(self):
        """Remove selected files from the index"""
        selected_indices = self.documents_listbox.curselection()
        if not selected_indices:
            logger.warning("Attempted to remove files, but no files were selected.")
            return
        if selected_indices:
            selected_files = [self.documents_listbox.get(i) for i in selected_indices]
            logger.info(f"Removing selected files: {selected_files}")
            self.controller.remove_files_from_index(selected_files)

            # Remove items from the listbox in reverse order to ensure indices don't change
            for index in reversed(selected_indices):
                self.documents_listbox.delete(index)

    def populate_listbox(self, filenames):
        for file in filenames:
            self.documents_listbox.insert(tk.END, file)
        logger.debug(f"Populated listbox with {len(filenames)} files.")

    def get_selected_files(self):
        return [self.documents_listbox.get(i) for i in self.documents_listbox.curselection()]
