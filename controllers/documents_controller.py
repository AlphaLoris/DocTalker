class DocumentsController:
    def __init__(self, app_controller, documents_model, documents_view):
        self.app_controller = app_controller
        self.model = documents_model
        self.view = documents_view
        self.view.set_controller(self)

    def set_docs_directory(self, directory):
        """Save the provided directory path to the model."""
        self.model.set_directory(directory)

    def get_docs_directory(self):
        """Get the currently saved directory path from the model."""
        return self.model.get_directory()

    def add_files(self, files):
        """Add files to the model."""
        self.model.add_files(files)

    def get_loaded_files(self):
        """Get the list of loaded files from the model."""
        return self.model.get_files()

    def remove_files_from_index(self, files):
        """Remove specific files from the model."""
        self.model.remove_files(files)
