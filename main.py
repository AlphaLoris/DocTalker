# main.py module

# Import necessary libraries and functions
from utils.log_config import setup_colored_logging
import logging
from controllers.application_controller import ApplicationController

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Environment Location:  C:\Users\glenn\anaconda3\envs\doctalker_faiss_2
# Activation command:  conda activate doctalker_faiss_2


# Main function
def main():
    setup_colored_logging()
    logger.info("Starting the application...")  # Example log message
    app_controller = ApplicationController()
    # app_controller.window.mainloop()
    logger.info("Application initialized.")  # Another example log message


if __name__ == "__main__":
    main()
