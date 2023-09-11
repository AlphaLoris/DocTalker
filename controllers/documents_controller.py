from utils.log_config import setup_colored_logging
import logging

# Set up logging
setup_colored_logging()
logger = logging.getLogger(__name__)


class DocumentsController:
    def __init__(self, app_controller, documents_model, documents_view):
        logger.debug("Initializing DocumentsController")
        self.app_controller = app_controller
        self.model = documents_model
        self.view = documents_view
        self.view.set_controller(self)

    def set_docs_directory(self, directory):
        logger.debug(f"Setting the documents directory to {directory}")
        """Save the provided directory path to the model."""
        self.model.set_directory(directory)

    def get_docs_directory(self):
        logger.debug(f"Getting the documents directory from the model.")
        """Get the currently saved directory path from the model."""
        return self.model.get_directory()

    def add_files(self, files):
        logger.debug(f"Adding files to the file library. Adding them to the model and then the index.")
        """Add files to the index in the model."""
        self.model.add_files(files)

    def get_loaded_files(self):
        logger.debug(f"Getting the list of loaded files from the model.")
        """Get the list of loaded files from the model."""
        return self.model.get_files()

    def remove_files_from_index(self, files):
        logger.debug(f"Removing files from the file library. Removing them from the model and then the index.")
        """Remove specific files from the model."""
        self.model.remove_files(files)
