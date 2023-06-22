import yaml
import json
import os


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


def assign_property(properties, property_name, value):
    keys = property_name.split('.')
    val = properties
    for key in keys[:-1]:
        val = val[key]
    val[keys[-1]] = value


class PropertiesModel:
    def __init__(self, filepath, context_windows):
        self.api_key = None
        self.working_files_path = None
        self.context_length = None
        self.model = None
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
        self.properties = self.load_properties(filepath)
        self.context_windows = context_windows


    def load_properties(self, filepath):
        try:
            with open(filepath, 'r') as file:
                properties = yaml.safe_load(file)
                if properties is None:
                    # Handle the case where the file is empty or only contains comments
                    properties = {}
        except FileNotFoundError:
            print(f"Properties file not found at {filepath}.")
            properties = {}
        except Exception as e:
            print(f"Could not load properties file due to error: {str(e)}")
            properties = {}
        return properties

    def persist_properties(self, properties, filepath):
        try:
            with open(filepath, 'w') as file:
                yaml.safe_dump(properties, file)
        except Exception as e:
            print("Could not write to properties file. Error: ", str(e))

    def extract_property(self, properties, property_name):
        keys = property_name.split('.')
        val = properties
        for key in keys:
            val = val[key]
        return val

    def update_context_length(self, *args):
        selected_model = self.model
        print("Updating context window value for selected model: " + selected_model)
        if selected_model in self.context_windows:
            context_length = self.context_windows[selected_model]
        else:
            context_length = 0
        self.context_length = context_length
        print("Context window value updated to: " + str(context_length))
        return context_length

    def validate_and_create_path(self, working_files_path):
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
                except OSError as e:
                    raise ValueError(f"Could not create directory '{current_path}': {e.strerror}")

    def set_properties(self, properties):
        errors = []
        for key, value in properties.items():
            if key == "api_key":
                self.api_key = value
                self.properties['api_key'] = value
                print("API Key set to: " + value)
            if key == "working_files_path":
                try:
                    if not value.strip():  # Check if the string is empty or only contains whitespaces
                        raise ValueError("Working files path cannot be empty")
                    self.validate_and_create_path(value)
                    self.working_files_path = value
                except ValueError as e:
                    errors.append(str(e))
            if key == "model":
                self.model = value
                self.context_length = self.update_context_length()
            if key == "temperature":
                try:
                    self.temperature = float(value)
                    if self.temperature < 0 or self.temperature > 2:
                        raise ValueError("Invalid temperature value")
                except ValueError:
                    errors.append(
                        f"Invalid temperature value entered for {key}: {value}. "
                        f"Please set temperature to a value in the range 0-2.")

            if key == "top_p":
                try:
                    self.top_p = float(value)
                    if self.top_p < 0 or self.top_p > 1:
                        raise ValueError("Invalid top_p value")
                except ValueError:
                    errors.append(
                        f"Invalid top_p value entered for {key}: {value}. "
                        f"Please set top_p to a value in the range 0-1.")

            if key == "n":
                try:
                    self.n = int(value)
                    if self.n < 1 or self.n > 4:
                        raise ValueError("Invalid n value")
                except ValueError:
                    errors.append(
                        f"Invalid n value entered for {key}: {value}. Please set n to a value in the range 1-4.")

            if key == "stream":
                self.stream = value

            if key == "stop":
                try:
                    self.stop = [s.strip().strip('\'"') for s in value.split(',')]
                    if len(self.stop) > 4:
                        raise ValueError("Too many stop sequences")
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
                        if self.max_tokens < 1 or self.max_tokens > self.context_windows:
                            raise ValueError("Invalid max_tokens value")
                except ValueError:
                    errors.append(
                        f"Invalid max_tokens value entered for {key}: {value}. "
                        f"Please set max_tokens to an empty value or a value in the range between 1 and"
                        f" {self.context_windows}.")

            if key == "presence_penalty":
                try:
                    self.presence_penalty = float(value)
                    if self.presence_penalty < -2.0 or self.presence_penalty > 2.0:
                        raise ValueError("Invalid presence_penalty value")
                except ValueError:
                    errors.append(
                        f"Invalid presence_penalty value entered for {key}: {value}. "
                        f"Please set presence_penalty to a value in the range -2 to 2.")

            if key == "frequency_penalty":
                try:
                    self.frequency_penalty = float(value)
                    if self.frequency_penalty < -2.0 or self.frequency_penalty > 2.0:
                        raise ValueError("Invalid frequency_penalty value")
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
                except json.JSONDecodeError:
                    errors.append(
                        f"Invalid JSON string entered for {key}: {value}. Please ensure it is a valid JSON string.")

            if key == "user":
                try:
                    if len(value) > 256:
                        raise ValueError("User value exceeds 256 characters")
                    else:
                        self.user = value
                except ValueError:
                    errors.append(
                        f"Invalid user value entered for {key}: {value}. "
                        f"Please ensure the user value does not exceed 256 characters.")

        if errors:
            raise ValueError("\n".join(errors))
