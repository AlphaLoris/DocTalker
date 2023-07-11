import logging


class PropertiesController:
    def __init__(self, application_controller, properties_model, properties_view, context_windows):
        self.app_controller = application_controller
        self.model = properties_model
        self.view = properties_view
        self.context_windows = context_windows
        # Updated to use attribute access instead of dictionary access
        if not self.model.working_files_path or not self.model.api_key:
            print("Properties not set; getting properties from user... ")
            properties_view.set_properties_controller(self)
            self.view.get_properties_from_user()
        # else:
        #     print("Properties set; continuing initialization... ")
        #     self.app_controller.continue_initialization()

    def handle_submit(self):
        properties = self.view.get_properties()
        try:
            self.model.set_properties(properties)
            # Persist the properties now that they are set
            self.model.persist_properties()
        except ValueError as e:
            self.view.show_error_message(str(e))
        except Exception as e:
            self.view.show_error_message("An unexpected error occurred: " + str(e))
        else:
            self.view.close_window()
            self.app_controller.continue_initialization()

    def get_properties(self):
        return {
            'working_files_path': self.model.working_files_path,
            'api_key': self.model.api_key,
            'llm_model': self.model.llm_model,
            'context_length': self.model.context_length,
            'user': self.model.user,
            'logit_bias': self.model.logit_bias,
            'frequency_penalty': self.model.frequency_penalty,
            'presence_penalty': self.model.presence_penalty,
            'max_tokens': self.model.max_tokens,
            'stream': self.model.stream,
            'n': self.model.n,
            'stop': self.model.stop,
            'top_p': self.model.top_p,
            'temperature': self.model.temperature,
            'context_windows': self.model.context_windows,
            'model_list': self.model.model_list
        }

    def get_property(self, property_name):
        logging.info("Getting property: %s", property_name)
        # Updated to use attribute access instead of dictionary access
        property_value = getattr(self.model, property_name, None)
        logging.info("Property value: %s", property_value)
        return property_value

    def set_property(self, property_name, value):
        print("Setting property:", property_name, "to", value)
        try:
            # Using set_properties method for validation
            self.model.set_properties({property_name: value})  # Wrapping the property_name and value in a dictionary
        except ValueError as e:
            print("Error setting property:", str(e))
        else:
            # If successful, print the updated value
            updated_value = getattr(self.model, property_name, None)
            print("Property value:", updated_value)
            return updated_value
