import yaml
import json
import os
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)

# working_files_path (r'C:\Users\glenn\DocTalker\')
#     doctalker_faiss_index
#     doctalker_indexed_document_nodes.txt
# Application Logs Path (r'C:\Users\glenn\DocTalker\Logs\')
# Chat history file path (r'C:\Users\glenn\DocTalker\ChatHistories\')
# Source Documents Directory
# API Key - Does this mean the file should be encrypted?
# Model custom parameters (these will be updated by the user during execution)
#     temperature = 0.7
#     top_p = 1.0
#     n = 1
#     stream = False - need to re-evaluate this one
#     stop = ""
#     max_tokens = ""
#     presence_penalty = ""
#     frequency_penalty = ""
#     logit_bias = ""
#     user = ""


class FileOperations:
    def __init__(self, filepath):
        logger.debug("Initializing FileOperations in properties_model.py module")
        self.filepath = filepath

    def load_properties(self):
        logger.debug(f"Loading properties from file {self.filepath} in properties_model.py module")
        try:
            with open(self.filepath, 'r') as file:
                properties = yaml.safe_load(file)
                if properties is None:
                    # Handle the case where the file is empty or only contains comments
                    logger.error(f"Properties file {self.filepath} is empty or only contains comments.")
                    return {}
                logger.info(f"Properties loaded from {self.filepath}.")
                logger.info(json.dumps(properties, indent=4))
                return properties
        except FileNotFoundError:
            logger.error(f"Properties file not found at {self.filepath}.")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing the properties file: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Could not load properties file due to an unexpected error: {str(e)}")
            return {}

    def persist_properties(self, properties):
        logger.debug(f"Persisting properties to file {self.filepath} in properties_model.py module")
        try:
            with open(self.filepath, 'w') as file:
                yaml.safe_dump(properties, file)
        except IOError as e:
            logger.error(f"Could not write to the properties file due to I/O error: {str(e)}")
        except yaml.YAMLError as e:
            logger.error(f"Could not write to the properties file due to YAML error: {str(e)}")
        except Exception as e:
            logger.error("Could not write to properties file due to an unexpected error: ", str(e))


class PropertiesModel:
    def __init__(self, filepath, context_windows):
        logger.debug("Initializing PropertiesModel in properties_model.py module")
        self.file_operations = FileOperations(filepath)
        self.api_key = None
        self.working_files_path = None
        self.context_length = None
        self.llm_model = None
        self.user = None
        self.logit_bias = None
        self.frequency_penalty = None
        self.presence_penalty = None
        self.max_tokens = None
        self.stream = None
        self.n = None
        self.stop = None
        self.top_p = None
        self.temperature = None
        self.context_windows = context_windows
        self.model_list = None

        # Load properties from file
        logger.debug(f"Attempting to loading properties from file {filepath} in properties_model.py module")
        properties = self.file_operations.load_properties()

        # Assign properties to attributes
        logger.debug(f"Assigning properties to attributes in properties_model.py module")
        self.api_key = properties.get('api_key')
        self.working_files_path = properties.get('working_files_path')
        self.context_length = properties.get('context_length')
        self.llm_model = properties.get('model')
        self.user = properties.get('user')
        self.logit_bias = properties.get('logit_bias')
        self.frequency_penalty = properties.get('frequency_penalty')
        self.presence_penalty = properties.get('presence_penalty')
        self.max_tokens = properties.get('max_tokens')
        self.stream = properties.get('stream')
        self.n = properties.get('n')
        self.stop = properties.get('stop')
        self.top_p = properties.get('top_p')
        self.temperature = properties.get('temperature')
        self.model_list = properties.get('model_list')

    def persist_properties(self):
        logger.debug("Persisting properties in properties_model.py module")
        # Store properties in a dictionary
        properties = {
            'api_key': self.api_key,
            'working_files_path': self.working_files_path,
            'context_length': self.context_length,
            'model': self.llm_model,
            'user': self.user,
            'logit_bias': self.logit_bias,
            'frequency_penalty': self.frequency_penalty,
            'presence_penalty': self.presence_penalty,
            'max_tokens': self.max_tokens,
            'stream': self.stream,
            'n': self.n,
            'stop': self.stop,
            'top_p': self.top_p,
            'temperature': self.temperature,
            'model_list': self.model_list
        }

        # Save properties to file
        logger.debug(f"Attempting to persist properties to file {self.file_operations.filepath}"
                     f" in properties_model.py module")
        try:
            self.file_operations.persist_properties(properties)
        except Exception as e:
            logger.error(f"Could not persist properties to file due to an unexpected error: {str(e)}")

    def update_context_length(self, *args):
        logger.debug("Updating context window value in properties_model.py module")
        context_length = 0
        selected_model = self.llm_model
        logger.info("Updating context window value for selected model: " + selected_model)
        try:
            if selected_model in self.context_windows:
                context_length = self.context_windows[selected_model]
                logger.info(f"Context window value for {selected_model} set to {context_length}")
            else:
                self.context_length = 4096
                raise ValueError(f"Model {selected_model} not found in context_windows")
            logger.error(f"Model {selected_model} not found in context_windows. Using default minimum value of"
                         f" {context_length}.")
        except ValueError as e:
            logger.error(f"An error occurred: {e}")
        return context_length

    def validate_and_create_path(self, working_files_path):
        logger.debug("Validating and creating path in properties_model.py module")
        # Normalize the path and split it into its directories
        path_parts = os.path.normpath(working_files_path).split(os.sep)

        # Start from the root directory (or the drive on Windows)
        current_path = path_parts[0] + os.sep if os.name == 'nt' else os.sep

        # For each directory in the path...
        for part in path_parts[1:]:
            # Add the directory to the current path
            current_path = os.path.join(current_path, part)

            # If this directory doesn't exist...
            if not os.path.exists(current_path):
                try:
                    # Try to create it
                    os.mkdir(current_path)
                    logger.info(f"Path {working_files_path} validated and created successfully.")
                except OSError as e:
                    raise ValueError(f"Could not create directory '{current_path}': {e.strerror}")

    def set_properties(self, properties):
        logger.debug("Setting properties in properties_model.py module")
        errors = []
        for key, value in properties.items():
            if key == "api_key":
                self.api_key = value
                logger.info("API Key set to: " + value)
            if key == "working_files_path":
                try:
                    if not value.strip():  # Check if the string is empty or only contains whitespaces
                        raise ValueError("Working files path cannot be empty")
                    self.validate_and_create_path(value)
                    logger.info("Working files path set to: " + value)
                    self.working_files_path = value
                except ValueError as e:
                    errors.append(str(e))
            if key == "model":
                self.llm_model = value
                self.context_length = self.update_context_length()
                logger.info("Model set to: " + value)
            if key == "temperature":
                try:
                    self.temperature = float(value)
                    if self.temperature < 0 or self.temperature > 2:
                        raise ValueError("Invalid temperature value")
                    logger.info("Temperature set to: " + str(self.temperature))
                except ValueError:
                    errors.append(
                        f"Invalid temperature value entered for {key}: {value}. "
                        f"Please set temperature to a value in the range 0-2.")
            if key == "top_p":
                try:
                    self.top_p = float(value)
                    if self.top_p < 0 or self.top_p > 1:
                        raise ValueError("Invalid top_p value")
                    logger.info("Top_p set to: " + str(self.top_p))
                except ValueError:
                    errors.append(
                        f"Invalid top_p value entered for {key}: {value}. "
                        f"Please set top_p to a value in the range 0-1.")
            if key == "n":
                try:
                    self.n = int(value)
                    if self.n < 1 or self.n > 4:
                        raise ValueError("Invalid n value")
                    logger.info("n set to: " + str(self.n))
                except ValueError:
                    errors.append(
                        f"Invalid n value entered for {key}: {value}. Please set n to a value in the range 1-4.")
            if key == "stream":
                self.stream = value
                logger.info("Stream set to: " + value)
            if key == "stop":
                try:
                    self.stop = [s.strip().strip('\'"') for s in value.split(',')]
                    if len(self.stop) > 4:
                        raise ValueError("Too many stop sequences")
                    logger.info("Stop set to: " + str(self.stop))
                except ValueError:
                    errors.append(
                        f"Invalid stop string entered for {key}: {value}. "
                        f"Please ensure the stop string does not include more than four stop sequences")
            if key == "max_tokens":
                try:
                    if value == '':
                        self.max_tokens = None
                    else:
                        self.max_tokens = int(value)
                        if self.max_tokens < 1 or self.max_tokens > self.context_windows[self.llm_model]:
                            raise ValueError("Invalid max_tokens value")
                        logger.info("Max tokens set to: " + str(self.max_tokens))
                except ValueError:
                    errors.append(
                        f"Invalid max_tokens value entered for {key}: {value}. "
                        f"Please set max_tokens to an empty value or a value in the range between 1 and"
                        f" {self.context_windows}.")
            if key == "presence_penalty":
                if value == '':
                    # Assign a special value or process as needed
                    self.presence_penalty = None
                else:
                    try:
                        self.presence_penalty = float(value)
                        if self.presence_penalty < -2.0 or self.presence_penalty > 2.0:
                            raise ValueError("Invalid presence_penalty value")
                        logger.info("Presence penalty set to: " + str(self.presence_penalty))
                    except ValueError:
                        errors.append(
                            f"Invalid presence_penalty value entered for {key}: {value}. "
                            f"Please set presence_penalty to a value in the range -2 to 2.")
            if key == "frequency_penalty":
                if value == '':
                    # Assign a special value or process as needed
                    self.frequency_penalty = None
                else:
                    try:
                        self.frequency_penalty = float(value)
                        if self.frequency_penalty < -2.0 or self.frequency_penalty > 2.0:
                            raise ValueError("Invalid frequency_penalty value")
                        logger.info("Frequency penalty set to: " + str(self.frequency_penalty))
                    except ValueError:
                        errors.append(
                            f"Invalid frequency_penalty value entered for {key}: {value}. "
                            f"Please set frequency_penalty to a value in the range -2 to 2.")
            if key == "logit_bias":
                try:
                    if value.strip() == '':
                        self.logit_bias = {}
                    else:
                        self.logit_bias = json.loads(value)
                        logger.info("Logit bias set to: " + str(self.logit_bias))
                except json.JSONDecodeError:
                    errors.append(
                        f"Invalid JSON string entered for {key}: {value}. Please ensure it is a valid JSON string.")
            if key == "user":
                try:
                    if len(value) > 256:
                        raise ValueError("User value exceeds 256 characters")
                    else:
                        self.user = value
                        logger.info("User set to: " + value)
                except ValueError:
                    errors.append(
                        f"Invalid user value entered for {key}: {value}. "
                        f"Please ensure the user value does not exceed 256 characters.")
            if key == "model_list":
                missing_models = [model for model in value if model not in self.context_windows]
                if missing_models:
                    errors.append(
                        f"The following models are not in the context_windows list: {', '.join(missing_models)}"
                    )
                else:
                    self.model_list = value
                    logger.info("Model list set to: " + str(self.model_list))

        if errors:
            raise ValueError("\n".join(errors))
