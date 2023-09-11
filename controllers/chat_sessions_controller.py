from models.chat_session_model import ChatSessionModel
from views.chat_session_view import ChatSessionView
from controllers.chat_session_controller import ChatSessionController
from controllers.llm_controller_pkg import LLMController
from models.llm_model import LLM_Model
from views.llm_view import LLMView
import tkinter as tk
from tkinter import ttk
from views.chat_sessions_view import LaunchWindow
from utils.log_config import setup_colored_logging
import logging

# Set up logging
setup_colored_logging()
logger = logging.getLogger(__name__)


class ChatSessionsController:
    def __init__(self, app_controller, properties_controller, chat_sessions_model, chat_sessions_view, parent):
        logger.debug("Initializing ChatSessionsController")
        self.name = None
        self.email = None
        self.organization = None
        self.parent = parent
        self.chat_session_window = None
        self.window = None
        self.chat_session_notebook = None
        self.app_controller = app_controller
        self.properties_controller = properties_controller
        self.chat_sessions_model = chat_sessions_model
        self.view = chat_sessions_view
        self.chat_sessions = []
        self.launch_window = None

    def initiate_chat_session(self):
        logger.debug("Initiating chat session by creating chat session window.")
        self.launch_window = LaunchWindow(parent=self.view, controller=self)
        logger.debug("Chat session window created.")

    def open_chat_session(self):
        logger.debug("Opening chat session by capturing the user's email, name, and organization.")
        # TODO: Update this to validate the user's email address, name, and organization
        email = self.launch_window.email_entry.get()
        name = self.launch_window.name_entry.get()
        organization = self.launch_window.org_entry.get()
        logger.debug(f"Attempting to launch chat session. Email: {email}, Name: {name}, Organization: {organization}")
        self.launch_chat_session(email, name, organization)
        logger.debug("Chat session successfully launched.")
        self.launch_window.destroy()

    # TODO: Add much more detailed logging to this method
    def launch_chat_session(self, email, name, organization):
        logger.debug("Launching chat session")
        self.email = email
        self.name = name
        self.organization = organization
        self.chat_session_window = tk.Toplevel(self.parent)
        self.chat_session_window.title("Chat Session")
        self.chat_session_window.geometry("800x600")

        self.chat_session_notebook = ttk.Notebook(self.chat_session_window)
        self.chat_session_notebook.pack(fill=tk.BOTH, expand=1)

        chat_session_model = ChatSessionModel(self.email, self.name, self.organization)
        chat_session_view = ChatSessionView(self.chat_session_notebook)
        chat_session_view.pack(fill=tk.BOTH, expand=True)
        chat_session_view.initiate_chat_session()

        # Create the LLMModel and LLMView, add the LLM View to the notebook and pack it within the intermediate frame
        llm_model_properties = self.properties_controller.get_properties()
        logger.info("llm properties retrieved from the properties controller. Creating the llm MVC components: ",
                    llm_model_properties)
        llm_model = LLM_Model(llm_model_properties)
        llm_view = LLMView(self.chat_session_notebook)  # Pass llm_tab_frame as the parent
        llm_view.pack(fill=tk.BOTH, expand=True)
        llm_controller = LLMController(llm_model, llm_view)
        llm_view.set_llm_controller(llm_controller)
        self.chat_session_notebook.add(chat_session_view, text="Chat Session")
        self.chat_session_notebook.add(llm_view, text="LLM Parameters")

        chat_session_controller = ChatSessionController(self, chat_session_model, chat_session_view, llm_controller)
        chat_session_view.set_chat_session_controller(chat_session_controller)
        llm_controller.set_chat_session_controller(chat_session_controller)

        # Register the chat sessions controller as an observer of the chat session model
        chat_session_model.register_observer(self.view)

        # Add this chat session to list of chat sessions
        self.chat_sessions.append(chat_session_controller)

        # Notify observers
        chat_session_model.notify_observers()
        llm_view.set_initial_state()
        logger.debug("Chat session launched.")

    def end_chat_session(self):
        logger.debug("Ending chat session")
        pass

    def update(self, chat_session):
        # This method will be called when a chat session is created
        print("Chat session created:", chat_session)

# User clicks on "New Chat Session" button
# Chat sessions controller creates a new chat session controller, model and view
# Chat sessions controller registers itself as an observer of the chat session model
# Chat sessions controller adds the chat session controller to its list of chat sessions
# Chat session controller updates the chat session model with the info about the new chat session
# Chat session model updates its observers (chat sessions controller) with the new chat session info
# Chat sessions controller updates its model with the new chat session info
# Chat sessions model updates notifies is observer (chat sessions view) with the new chat session info
# Chat sessions view updates its list of chat sessions with the new chat session info
# The user enters a query in the chat session view and submits it to the chat session controller
# The chat session controller validates the query. If it is valid, it updates the chat session model with the query
# The chat session model updates its chat history with the new query
# The chat session model updates its observer (chat session view) with the new query
# The chat session view updates its chat history with the new query
# The chat session model embeds the query and performs a semantic search using the query
# The chat session model assembles the search result into a prompt
# The chat session passes the query and the prompt to the LLM controller
# The LLM controller submits the prompt to the LLM model
# The LLM controller updates the history of prompts
# The LLM model generates a response to the prompt
# The LLM model validates the response and iterates (with human input?) until the response is valid
# The LLM identifies when it can't answer the query using the semantic search result
# If semantic search result does not speak to the query,
#    the query is added to the list of questions that need to be answered in the documents
# The LLM model passes its response to the LLM controller
# The LLM controller updates chat controller with the response
# The LLM controller updates the Chat Session model with the response
# The Chat Session model updates its chat history with the response
# The Chat Session model notifies view of the update to its chat
# The Chat Session view updates its chat history with the response



