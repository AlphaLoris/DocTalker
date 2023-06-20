from models.properties_model import PropertiesModel
from views.properties_view import PropertiesView


class PropertiesController:
    def __init__(self, parent, filepath, context_windows):
        self.model = PropertiesModel(filepath, context_windows)
        self.view = PropertiesView(self, parent, context_windows)
        if not self.model.properties.get('working_files_path') or not self.model.properties.get('api_key'):
            self.view.get_properties_from_user()

    # in your Controller class
    def handle_submit(self):
        properties = self.view.get_properties()  # view's method to return self.properties
        try:
            self.model.set_properties(properties)  # model's method to set properties based on a dictionary
        except ValueError as e:
            self.view.show_error_message(str(e))  # view's method to show an error message
        else:
            self.view.close_window()


    def get_property(self, property_name):
        return self.model.properties.get(property_name)
