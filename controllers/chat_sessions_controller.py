from models.chat_sessions_model import ChatSessionsModel


class ChatSessionsController:
    def __init__(self, app_controller, parent):
        self.app_controller = app_controller
        self.model = ChatSessionsModel()
        pass
