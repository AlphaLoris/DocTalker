from models.chat_sessions_model import ChatSessionsModel
from views.chat_sessions_view import ChatSessionsView
from models.chat_session_model import ChatSessionModel
from controllers.chat_session_controller import ChatSessionController


class ChatSessionsController:
    def __init__(self, app_controller, parent):
        self.app_controller = app_controller
        self.parent = parent
        self.model = ChatSessionsModel()
        self.view = ChatSessionsView(parent, self)
        self.chat_sessions = []

    def launch_chat_session(self):
        chat_session = ChatSessionModel()
        chat_session_controller = ChatSessionController(chat_session, self.parent)
        # Register as an observer
        chat_session.register_observer(self)
        # Add to list of chat sessions
        self.chat_sessions.append(chat_session_controller)
        # Notify observers
        chat_session.notify_observers()

    def update(self, chat_session):
        # This method will be called when a chat session is created
        print("Chat session created:", chat_session)
