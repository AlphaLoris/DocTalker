from tkinter import messagebox
from controllers.llm_controller import LLMController
# from utils.node import generate_unique_id

# TODO: Assign each chat session a unique ID and use it in API calls
# TODO: Get user email address at the start of each chat session


class ChatSessionController:
    def __init__(self, chat_sessions_controller, chat_session_model, chat_session_view):
        self.app_controller = chat_sessions_controller
        self.model = chat_session_model
        self.view = chat_session_view
        # TODO: Pass the llm_controller In from the chat_sessions_controller
        self.llm_controller = LLMController()
        # self.guid = generate_unique_id()

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

    def submit_chat_text(self, chat_text):
        # if self.validate_chat_text(chat_text) and self.validate_chat_length(chat_text):

        pass



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
