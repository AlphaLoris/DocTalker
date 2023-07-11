import logging
import tkinter as tk
from tkinter import ttk
from controllers.chat_sessions_controller import ChatSessionsController
from controllers.documents_controller import DocumentsController
from controllers.properties_controller import PropertiesController
from models.documents_model import DocumentsModel
from models.chat_sessions_model import ChatSessionsModel
from models.properties_model import PropertiesModel
from views.documents_view import DocumentsView
from views.chat_sessions_view import ChatSessionsView
from views.properties_view import PropertiesView


class ApplicationController:
    def __init__(self):
        # Create a root window but keep it hidden
        self.chat_sessions_view = None
        self.documents_view = None
        self.root = tk.Tk()
        self.root.withdraw()
        self.window = None
        self.view = None
        self.documents_controller = None
        self.chat_sessions_controller = None
        self.documents_model = DocumentsModel()
        self.chat_sessions_model = ChatSessionsModel()
        self.notebook = None
        logger = logging.getLogger(__name__)
        logger.info("Initializing Application Controller and creating main window.")

        context_windows = {
            "gpt-4": 8192,
            "gpt-4-0613": 8192,
            "gpt-4-0314": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-32k-0613": 32768,
            "gpt-4-32k-0314": 32768,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384,
            "gpt-3.5-turbo-0613": 4096,
            "gpt-3.5-turbo-0301": 4096
        }
        properties_model = PropertiesModel(r'C:\Users\glenn\DocTalker\properties.yaml', context_windows)
        properties_view = PropertiesView(self, self.root, context_windows)
        """
        self.properties_controller = PropertiesController(self, properties_model, properties_view, context_windows)
        properties_view.set_properties_controller(self.properties_controller)
        print("Properties controller initialized. Starting main loop.")
        # Start the Tkinter main loop
        self.root.mainloop()
        """
        self.properties_controller = PropertiesController(self, properties_model, properties_view, context_windows)
        properties_view.set_properties_controller(self.properties_controller)
        print("Properties controller initialized.")
        if self.properties_controller.model.working_files_path and self.properties_controller.model.api_key:
            print("Properties set; continuing initialization... ")
            self.continue_initialization()
        else:
            print("Properties not set; starting main loop...")
            self.root.mainloop()

    def continue_initialization(self):
        # Main window
        self.window = tk.Tk()
        self.window.title("DocTalker LLM AI Chatbot")
        self.window.geometry("1000x770")

        # Notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.chat_sessions_view = ChatSessionsView(self.notebook)
        self.chat_sessions_controller = ChatSessionsController(self, self.properties_controller,
                                                               self.chat_sessions_model, self.chat_sessions_view,
                                                               self.window)
        self.chat_sessions_view.set_controller(self.chat_sessions_controller)
        self.documents_view = DocumentsView(self.notebook)
        self.documents_controller = DocumentsController(self, self.documents_model, self.documents_view)
        self.documents_view.set_controller(self.documents_controller)

        # Adding tabs
        self.notebook.add(self.chat_sessions_controller.view, text="Chat Sessions")
        self.notebook.add(self.documents_controller.view, text="Documents")

        self.view = self.window

        # Start the main event loop of Tkinter
        self.window.mainloop()

