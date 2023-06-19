import tkinter as tk
import yaml

"""
Working list of properties:
working_files_path
api_key
# Model custom parameters (these will be updated by the user during execution)
temperature
top_p
n
stream
stop
max_tokens
presence_penalty
frequency_penalty
logit_bias
user
"""
    
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


class PropertiesModel:
    def __init__(self, filepath):
        self.filepath = filepath
        self.properties = self.load_properties(filepath)

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

    def extract_property(properties, property_name):
        keys = property_name.split('.')
        val = properties
        for key in keys:
            val = val[key]
        return val

    def assign_property(properties, property_name, value):
        keys = property_name.split('.')
        val = properties
        for key in keys[:-1]:
            val = val[key]
        val[keys[-1]] = value
