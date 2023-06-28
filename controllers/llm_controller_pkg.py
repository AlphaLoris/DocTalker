from models.llm_model import LLM_Model
from views.llm_view import LLMView
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from utils.open_ai_capabilities import is_valid_api_key


class LLMController:
    def __init__(self, llm_model, llm_view):
        self.chat_session_controller = None
        self.model = llm_model
        self.view = llm_view
        self.working_directory = None  # initialize the log directory to None
        self.api_key = None  # initialize the api key to None

    def set_chat_session_controller(self, chat_session_controller):
        self.chat_session_controller = chat_session_controller

    # Get and Set File Directory
    def browse_directory(self):
        # open a file dialog to allow the user to select a directory
        directory = tk.filedialog.askdirectory()
        if directory:
            # if a directory was selected, update the log_directory attribute
            self.working_directory = directory
            return directory
        return None

    def set_directory(self, directory):
        self.model.directory = directory
    # End of Get File Directory

    # Set API Key
    def set_api_key(self, api_key):
        if self.api_key is None:
            if self.validate_api_key(api_key):
                self.model.api_key = api_key
                return True
            else:
                return False
        elif self.model.name != api_key:
            if self.validate_api_key(api_key):
                self.model.api_key = api_key
                return True
            else:
                return False
        else:
            return True

    def validate_api_key(self, api_key):
        error_messages = is_valid_api_key(api_key)
        if error_messages:
            messagebox.showerror("Invalid API Key:", "Invalid API Key entered.\n" + "\n".join(error_messages))
            return False
        else:
            return True
    # End of Validate the API Key

    # Validate parameters. If the parameters are valid, set them in the model
    def set_parameters(self, parameters):
        errors = []

        for key, value in parameters.items():
            if value is None:
                errors.append(f"Invalid {key} value")

        if errors:
            return False, errors

        self.model.set_model_parameters(parameters)
        return True, None

    # End of Validate parameters.
