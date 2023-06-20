import yaml
import json

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
        self.filepath = filepath
        self.properties = self.load_properties(filepath)
        self.context_windows = context_windows

        # TODO:  Determine and set the context window for the selected model

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

    def set_properties(self, properties):
        errors = []
        for key, value in properties.items():
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
            raise ValueError(errors)

    """
    # in your Model class
    def set_properties(self, properties):
        for key, value in properties.items():
            if key == 'working_files_path':
                self.set_working_files_path(value)
            elif key == 'api_key':
                self.set_api_key(value)
            elif key == 'model':
                self.set_model(value)
            elif key == 'temperature':
                self.set_temperature(value)
            elif key == 'top_p':
                self.set_top_p(value)
            elif key == 'n':
                self.set_n(value)
            elif key == 'stream':
                self.set_stream(value)
            elif key == 'stop':
                self.set_stop(value)
            elif key == 'max_tokens':
                self.set_max_tokens(value)
            elif key == 'presence_penalty':
                self.set_presence_penalty(value)
            elif key == 'frequency_penalty':
                self.set_frequency_penalty(value)
            elif key == 'logit_bias':
                self.set_logit_bias(value)
            elif key == 'user':
                self.set_user(value)
            return
    """
