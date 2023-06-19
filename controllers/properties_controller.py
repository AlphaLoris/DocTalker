from models.properties_model import PropertiesModel
from views.properties_view import PropertiesView


class PropertiesController:
    def __init__(self, parent, filepath, context_windows):
        # Creates a model object. When the model object is created, it loads properties from the file if the file exists
        self.model = PropertiesModel(filepath)
        # Creates a view object and passes it a reference to the parent window
        self.view = PropertiesView(parent, context_windows)

        # If the properties file did not exist, and so the properties are not populated, then the system asks the user
        # to enter properties in update_properties
        if not self.model.properties.get('working_files_path') or not self.model.properties.get('api_key'):
            self.update_properties()

    def update_properties(self):
        # The view asks the user to enter properties by opening the properties pop-up window
        new_properties = self.view.get_properties_from_user()
        # The model persists the properties to the file
        self.model.persist_properties(new_properties, self.model.filepath)
        # The model updates its properties
        self.model.properties = new_properties

    def get_property(self, property_name):
        return self.model.properties.get(property_name)
