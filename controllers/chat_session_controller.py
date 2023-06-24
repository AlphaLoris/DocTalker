from tkinter import messagebox
from models.chat_session_model import ChatSessionModel
from views.chat_session_view import ChatSessionView

# TODO: Assign each chat session a unique ID and use it in API calls
# TODO: Get user email address at the start of each chat session


class ChatSessionController:
    def __init__(self, app_controller, parent):
        self.app_controller = app_controller
        self.model = ChatSessionModel()
        self.view = ChatSessionView(parent, self)

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

    def initiate_chat_session(self):
        self.view.initiate_chat_session()


    def submit_chat_text(self):
        chat_text = self.view.get_chat_text()
        if self.validate_chat_text(chat_text) and self.validate_chat_length(chat_text):
            self.view.submit_chat_text(chat_

# Initiate the chat session
# Assign the chat session a unique ID
# The user will be prompted to enter their email address
# The user will enter a query
# The query will be validated programmatically
#    - The query cannot be empty
#    - The query cannot be longer 60% of the context length
# The query will be validated by the model
#    - The query should be contextually relevant and aligned with the intent of the chat session
#    - The query should not be abusive or offensive
#    - The query should be comprehensible
