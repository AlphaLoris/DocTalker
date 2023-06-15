from tkinter import messagebox
from models.chat_model import ChatModel
from views.chat_view import ChatView

# TODO: Assign each chat session a unique ID and use it in API calls
# TODO: Get user email address at the start of each chat session
class ChatSessionController:
    def __init__(self, app_controller, parent):
        self.app_controller = app_controller
        self.model = ChatModel()
        self.view = ChatView(parent, self)

    def validate_chat_text(self, chat_text):
        if chat_text == "":
            messagebox.showerror("Error", "Chat text cannot be empty")
            return False
        else:
            return True

    def validate_chat_length(self, chat_text):
        if len(chat_text) > 200:
            messagebox.showerror("Error", "Chat text cannot be longer than 200 characters")
            return False
        else:
            return True