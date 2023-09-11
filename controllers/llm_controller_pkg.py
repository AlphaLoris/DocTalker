from models.llm_model import LLM_Model
from views.llm_view import LLMView
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from utils.open_ai_capabilities import is_valid_api_key
from utils.log_config import setup_colored_logging
import logging

# Set up logging
setup_colored_logging()
logger = logging.getLogger(__name__)


class LLMController:
    def __init__(self, llm_model, llm_view):
        logger.debug("Initializing LLMController")
        self.chat_session_controller = None
        self.model = llm_model
        self.view = llm_view
        self.working_directory = None  # initialize the log directory to None
        self.api_key = None  # initialize the api key to None

    def set_chat_session_controller(self, chat_session_controller):
        logger.debug("Setting chat_session_controller in LLMController")
        self.chat_session_controller = chat_session_controller

    # Get and Set File Directory
    def browse_directory(self):
        logger.debug("Browsing for directory in LLMController")
        # open a file dialog to allow the user to select a directory
        directory = tk.filedialog.askdirectory()
        if directory:
            # if a directory was selected, update the log_directory attribute
            self.working_directory = directory
            return directory
        return None

    def set_directory(self, directory):
        logger.debug("Setting directory in LLMController")
        self.model.directory = directory
    # End of Get File Directory

    # Set API Key
    def set_api_key(self, api_key):
        logger.debug("Setting API Key in LLMController")
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
        logger.debug("Validating API Key in LLMController")
        error_messages = is_valid_api_key(api_key)
        if error_messages:
            messagebox.showerror("Invalid API Key:", "Invalid API Key entered.\n" + "\n".join(error_messages))
            return False
        else:
            return True
    # End of Validate the API Key

    # Validate parameters. If the parameters are valid, set them in the model
    def set_parameters(self, parameters):
        logger.debug("Setting parameters in LLMController")
        errors = []

        for key, value in parameters.items():
            if value is None:
                errors.append(f"Invalid {key} value")

        if errors:
            return False, errors

        self.model.set_model_parameters(parameters)
        return True, None

    # End of Validate parameters.

    def get_property(self, property_name):
        logger.debug("Getting property in LLMController")
        """
        Get the value of a specific property from the model.

        Args:
            property_name (str): The name of the property to retrieve.

        Returns:
            The value of the property, or None if the property does not exist.
        """
        logger.info(f"Getting property in llm_controller from the llm_model: {property_name}")
        property_value = getattr(self.model, property_name, None)
        logger.info(f"Value of property returned for '{property_name}': {property_value}")
        return property_value
