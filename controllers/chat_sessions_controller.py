from models.chat_sessions_model import ChatSessionsModel
from views.chat_sessions_view import ChatSessionsView
from models.chat_session_model import ChatSessionModel
from views.chat_session_view import ChatSessionView
from controllers.chat_session_controller import ChatSessionController
import tkinter as tk


class ChatSessionsController:
    def __init__(self, app_controller, chat_sessions_model, chat_sessions_view):
        self.app_controller = app_controller
        self.model = chat_sessions_model
        self.view = chat_sessions_view
        self.chat_sessions = []

    def launch_chat_session(self):
        root = self.view.winfo_toplevel()
        chat_session_model = ChatSessionModel()
        chat_session_view = ChatSessionView(chat_session_model, root)
        chat_session_controller = ChatSessionController(self, chat_session_model, chat_session_view)
        chat_session_view.set_controller(chat_session_controller)
        # Register as an observer
        self.model.register_observer(self)
        # Add to list of chat sessions
        self.chat_sessions.append(chat_session_controller)
        # Notify observers
        self.model.notify_observers()

    def end_chat_session(self):
        pass

    def update(self, chat_session):
        # This method will be called when a chat session is created
        print("Chat session created:", chat_session)
