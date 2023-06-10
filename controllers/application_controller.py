import tkinter as tk
from tkinter import ttk
from controllers.chat_controller import ChatController
from controllers.llm_controller import LLMController
from controllers.documents_controller import DocumentsController


class ApplicationController:
    def __init__(self):
        # Main window
        self.window = tk.Tk()
        self.window.title("DocTalker LLM AI Chatbot")
        self.window.geometry("1000x770")

        # Notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.llm_controller = LLMController(self, self.notebook)
        self.chat_controller = ChatController(self, self.notebook)
        self.documents_controller = DocumentsController(self, self.notebook)

        # Adding tabs
        self.notebook.add(self.chat_controller.view, text="Chat")
        self.notebook.add(self.llm_controller.view, text="LLM")
        self.notebook.add(self.documents_controller.view, text="Documents")

        self.view = self.window
