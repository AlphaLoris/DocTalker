from models.properties_model import PropertiesModel
from views.properties_view import PropertiesView

import logging


class PropertiesController:
    def __init__(self, application_controller, parent, filepath, context_windows):
        self.model = PropertiesModel(filepath, context_windows)
        self.view = PropertiesView(self, parent, context_windows)
        self.app_controller = application_controller

        if not self.model.properties.get('working_files_path') or not self.model.properties.get('api_key'):
            self.view = PropertiesView(self, parent, context_windows)  # Pass the parent here
            self.view.get_properties_from_user()

    def handle_submit(self):
        properties = self.view.get_properties()
        try:
            self.model.set_properties(properties)
        except ValueError as e:
            self.view.show_error_message(str(e))
        except Exception as e:
            self.view.show_error_message("An unexpected error occurred: " + str(e))
        else:
            self.view.close_window()
            self.app_controller.continue_initialization()

    def get_property(self, property_name):
        logging.info("Getting property: %s", property_name)
        property_value = self.model.properties.get(property_name)
        logging.info("Property value: %s", property_value)
        return property_value

    def set_property(self, property_name, value):
        print("Setting property:", property_name, "to", value)
        try:
            # Using set_properties method for validation
            self.model.set_properties({property_name: value}) # Wrapping the property_name and value in a dictionary
        except ValueError as e:
            print("Error setting property:", str(e))
        else:
            # If successful, print the updated value
            print("Property value:", self.model.extract_property(self.model.properties, property_name)) # Changed this line to use extract_property method
            return self.model.extract_property(self.model.properties, property_name) # Changed this line to use extract_property method



