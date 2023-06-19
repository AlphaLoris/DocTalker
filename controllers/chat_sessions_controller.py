from models.chat_sessions_model import ChatSessionsModel
from views.chat_sessions_view import ChatSessionsView


class ChatSessionsController:
    def __init__(self, app_controller, parent):
        self.app_controller = app_controller
        self.model = ChatSessionsModel()
        self.view = ChatSessionsView(parent, self)
        pass
