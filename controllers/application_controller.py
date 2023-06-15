import logging
import tkinter as tk
from tkinter import ttk
from utils.property_operations import load_properties
from controllers.chat_sessions_controller  import ChatSessionsController
from controllers.llm_controller import LLMController
from controllers.documents_controller import DocumentsController


class ApplicationController:
    def __init__(self):
        logger = logging.getLogger(__name__)
        logger.info("Initializing Application Controller and creating main window.")

        # Main window
        self.window = tk.Tk()
        self.window.title("DocTalker LLM AI Chatbot")
        self.window.geometry("1000x770")

        # Notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.llm_controller = LLMController(self, self.notebook)
        self.chat_controller = ChatSessionsController(self, self.notebook)
        self.documents_controller = DocumentsController(self, self.notebook)
        self.properties_controller = PropertiesController(self.window, 'properties.yaml')

        # Adding tabs
        self.notebook.add(self.chat_controller.view, text="Chat")
        self.notebook.add(self.llm_controller.view, text="LLM")
        self.notebook.add(self.documents_controller.view, text="Documents")

        self.view = self.window

        """
        Working list of properties:
	    Working files path
	        Index
	        Indexed documents text
	    Application Logs Path
	    Raw Documents directory
        Chat history file path
	    API Key - Does this mean the file should be encrypted?
	    Model default parameters
		    temperature = 0.7
		    top_p = 1.0
		    n = 1
		    stream = False - need to re-evaluate this one
		    stop = ""
		    max_tokens = ""
		    presence_penalty = ""
		    frequency_penalty = ""
		    logit_bias = ""
            user = ""
        Model custom parameters
            temperature = 0.7temperature = 0.7
		    top_p = 1.0
		    n = 1
		    stream = False - need to re-evaluate this one
		    stop = ""
		    max_tokens = ""
		    presence_penalty = ""
		    frequency_penalty = ""
		    logit_bias = ""
            user = ""
        """
        logger.info("Attempting to load properties file.")
        # Load properties from a YAML file
        try:
            properties = load_properties(r'C:\Users\glenn\DocTalker\properties.yaml')
        except:


