from models.properties_model import PropertiesModel
from views.properties_view import PropertiesView


class PropertiesController:
    def __init__(self, parent, filepath):
        self.model = PropertiesModel(filepath)
        self.view = PropertiesView(parent)

        if not self.model.properties:
            self.update_properties()

    def update_properties(self):
        new_properties = self.view.get_properties_from_user()
        self.model.persist_properties(new_properties)
        self.model.properties = new_properties

    def get_property(self, property_name):
        return self.model.properties.get(property_name)