from tkinter import messagebox
from utils.log_config import setup_colored_logging
import logging

# Set up logging
setup_colored_logging()
logger = logging.getLogger(__name__)

# TODO: Assign each chat session a unique ID and use it in API calls
# TODO: Get user email address at the start of each chat session


class ChatSessionController:
    def __init__(self, chat_sessions_controller, chat_session_model, chat_session_view, llm_controller):
        logger.debug("Initializing ChatSessionController")
        self.chat_sessions_controller = chat_sessions_controller
        self.model = chat_session_model
        self.view = chat_session_view
        self.view.set_chat_session_controller(self)
        self.llm_controller = llm_controller
        # self.context_window = llm_controller.get_context_window()

    def validate_chat_text(self, chat_text):
        logger.debug("Validating chat text")
        if chat_text == "":
            messagebox.showerror("Error", "Chat text cannot be empty")
            logger.debug("Chat text was empty.")
            return False
        else:
            logger.debug("Chat text was valid (not empty).")
            return True

    def validate_chat_length(self, chat_text):
        logger.debug("Validating chat length")
        if len(chat_text) > 200:
            messagebox.showerror("Error", "Chat text cannot be longer than 200 characters")
            logger.debug("Chat text was too long (> 200 characters).")
            return False
        else:
            logger.debug("Chat text was valid (not longer than 200 characters).")
            return True

    def submit_chat_text(self, chat_text):
        logger.debug("Submitting chat text")
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


