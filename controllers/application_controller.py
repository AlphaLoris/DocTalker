import logging
import tkinter as tk
from tkinter import ttk
from controllers.chat_sessions_controller import ChatSessionsController
from controllers.llm_controller import LLMController
from controllers.documents_controller import DocumentsController
from controllers.properties_controller import PropertiesController


class ApplicationController:
    def __init__(self):
        self.view = None
        self.documents_controller = None
        self.chat_sessions_controller = None
        self.llm_controller = None
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

        # Main window
        self.window = tk.Tk()
        self.window.title("DocTalker LLM AI Chatbot")
        self.window.geometry("1000x770")

        self.properties_controller = PropertiesController(self, self.window, r'C:\Users\glenn\DocTalker\properties.yaml',
                                                          context_windows)

    def continue_initialization(self):
        # Notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.llm_controller = LLMController(self, self.notebook)
        self.chat_sessions_controller = ChatSessionsController(self, self.notebook)
        self.documents_controller = DocumentsController(self, self.notebook)

        # Adding tabs
        self.notebook.add(self.chat_sessions_controller.view, text="Chat Sessions")
        self.notebook.add(self.llm_controller.view, text="LLM")
        self.notebook.add(self.documents_controller.view, text="Documents")

        self.view = self.window



