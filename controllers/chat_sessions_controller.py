from models.chat_sessions_model import ChatSessionsModel
from views.chat_sessions_view import ChatSessionsView
from models.chat_session_model import ChatSessionModel
from views.chat_session_view import ChatSessionView
from controllers.chat_session_controller import ChatSessionController
from controllers.llm_controller_pkg import LLMController
from models.llm_model import LLM_Model
from views.llm_view import LLMView
import tkinter as tk
from tkinter import ttk


class ChatSessionsController:
    def __init__(self, app_controller, chat_sessions_model, chat_sessions_view, parent):
        self.parent = parent
        self.chat_session_window = None
        self.window = None
        self.chat_session_notebook = None
        self.app_controller = app_controller
        self.chat_session_model = chat_sessions_model
        self.view = chat_sessions_view
        self.chat_sessions = []

    def launch_chat_session(self, chat_session_tab_frame=None):
        self.chat_session_window = tk.Toplevel(self.parent)
        self.chat_session_window.title("Chat Session")
        self.chat_session_window.geometry("800x600")

        self.chat_session_notebook = ttk.Notebook(self.chat_session_window)
        self.chat_session_notebook.pack(fill=tk.BOTH, expand=1)

        chat_session_model = ChatSessionModel()
        chat_session_view = ChatSessionView(self.chat_session_notebook)
        chat_session_view.pack(fill=tk.BOTH, expand=True)
        chat_session_view.initiate_chat_session()


        # Create LLMView and pack it within the intermediate frame
        llm_model = LLM_Model()
        llm_view = LLMView(self.chat_session_notebook)  # Pass llm_tab_frame as the parent
        llm_view.pack(fill=tk.BOTH, expand=True)
        llm_controller = LLMController(llm_model, llm_view)
        llm_view.set_llm_controller(llm_controller)

        self.chat_session_notebook.add(chat_session_view, text="Chat Session")
        self.chat_session_notebook.add(llm_view, text="LLM Parameters")
        
        self.view = self.window

        chat_session_controller = ChatSessionController(self, chat_session_model, chat_session_view, llm_controller)
        chat_session_view.set_chat_session_controller(chat_session_controller)
        llm_controller.set_chat_session_controller(chat_session_controller)

        """
        # Register as an observer
        self.chat_session_model.register_observer(self)

        # Add to list of chat sessions
        self.chat_sessions.append(chat_session_controller)

        # Notify observers
        self.chat_session_model.notify_observers()
        """

    """
    def launch_chat_session(self):
        root = self.view.winfo_toplevel()
        chat_session_model = ChatSessionModel()
        chat_session_view = ChatSessionView(root)

        chat_session_view.initiate_chat_session()

        # Ensure that the notebook is properly initialized and packed
        assert chat_session_view.chat_session_notebook is not None, "Notebook is not initialized"

        # Create an intermediate frame that will be added as a tab
        llm_tab_frame = tk.Frame(chat_session_view.chat_session_notebook)  # Pass chat_session_notebook as the parent
        llm_tab_frame.pack(fill=tk.BOTH, expand=True)  # Ensure that the frame is packed

        # Create LLMView and pack it within the intermediate frame
        llm_model = LLM_Model()
        llm_view = LLMView(llm_tab_frame)  # Pass llm_tab_frame as the parent
        llm_view.pack(fill=tk.BOTH, expand=True)

        llm_controller = LLMController(llm_model, llm_view)
        llm_view.set_llm_controller(llm_controller)

        chat_session_controller = ChatSessionController(self, chat_session_model, chat_session_view, llm_controller)
        chat_session_view.set_chat_session_controller(chat_session_controller)

        # Add the intermediate frame as a tab
        chat_session_view.add_tab(llm_tab_frame, "LLM Parameters")

        llm_controller.set_chat_session_controller(chat_session_controller)

        # Register as an observer
        self.chat_session_model.register_observer(self)

        # Add to list of chat sessions
        self.chat_sessions.append(chat_session_controller)

        # Notify observers
        self.chat_session_model.notify_observers()

    def launch_chat_session(self):
        root = self.view.winfo_toplevel()
        chat_session_model = ChatSessionModel()
        chat_session_view = ChatSessionView(root)
        llm_model = LLM_Model()
        llm_view = LLMView()
        llm_controller = LLMController(llm_model, llm_view)
        llm_view.set_llm_controller(llm_controller)
        chat_session_controller = ChatSessionController(self, chat_session_model, chat_session_view, llm_controller)
        chat_session_view.set_chat_session_controller(chat_session_controller)
        chat_session_view.add_tab(llm_view, "LLM Parameters")
        llm_controller.set_chat_session_controller(chat_session_controller)
        # Register as an observer
        self.chat_session_model.register_observer(self)
        # Add to list of chat sessions
        self.chat_sessions.append(chat_session_controller)
        # Notify observers
        self.chat_session_model.notify_observers()
    """

    def end_chat_session(self):
        pass

    def update(self, chat_session):
        # This method will be called when a chat session is created
        print("Chat session created:", chat_session)
