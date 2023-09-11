from datetime import datetime
from utils.node import generate_unique_id
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)


class ChatSessionModel:
    def __init__(self, email_address, name, organization):
        logger.debug("Initializing ChatSessionModel")
        self.observers = []
        self.chat_session_id = generate_unique_id()
        self.user_email = email_address
        self.user_name = name
        self.user_organization = organization
        self.start_datetime = datetime.now()
        self.start_date = self.get_start_date()
        self.start_time = self.get_start_time()
        self.duration = None
        self.sentiment = None
        self.cost = None
        self.query_count = None
        self.prompt_count = None
        self.keywords = None

    #         - Chat session ID
    #         - User email address
    #         - User name
    #         - User organization
    #         - start date
    #         - start time
    #         - Duration of the chat session
    #         - Current sentiment of the chat session
    #         - Cost of each chat session
    #         - Number of user queries submitted in each chat session
    #         - Number of prompts submitted in each chat session
    #         - Keywords/Topics of each chat session

    def set_user_email(self, user_email):
        logger.debug(f"Setting user email: {user_email}")
        self.user_email = user_email

    def set_user_name(self, user_name):
        logger.debug(f"Setting user name: {user_name}")
        self.user_name = user_name

    def set_user_organization(self, user_organization):
        logger.debug(f"Setting user organization: {user_organization}")
        self.user_organization = user_organization

    def get_start_date(self):
        # Extract and return only the date part in string format
        self.start_date = self.start_datetime.strftime("%Y-%m-%d")
        logger.info(f"Setting start_date as: ", self.start_date)
        return self.start_date

    def get_start_time(self):
        # Extract and return only the time part in string format
        self.start_time = self.start_datetime.strftime("%H:%M:%S")
        logger.info(f"Setting start_time as: ", self.start_time)
        return self.start_time

    def calculate_duration(self):
        logger.debug("Calculating duration of session")
        current_datetime = datetime.now()
        duration = current_datetime - self.start_datetime

        # Extracting days, hours, minutes, and seconds from duration
        days = duration.days
        total_seconds = duration.seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        self.duration = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
        logger.info("Duration: ", self.duration)

    def calculate_session_cost(self):
        logger.debug("Calculating cost of session")
        pass

    def set_sentiment(self, sentiment):
        logger.debug(f"Setting sentiment: {sentiment}")
        self.sentiment = sentiment

    def increment_query_count(self):
        logger.debug("Incrementing query count")
        self.query_count += 1

    def increment_prompt_count(self):
        logger.debug("Incrementing prompt count")
        self.prompt_count += 1

    def add_keywords(self, keywords):
        logger.debug(f"Adding keywords: {keywords}")
        # only add keywords if they are not already in the list
        self.keywords.append(keywords)

    def register_observer(self, observer):
        logger.debug(f"Registering observer: {observer}")
        self.observers.append(observer)

    def notify_observers(self):
        logger.debug("Notifying observers")
        for observer in self.observers:
            observer.update_sessions(self)
