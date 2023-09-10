class DocumentsModel:
    def __init__(self):
        self._directory = None  # to store the path of the document source directory
        self._loaded_files = []  # to store the list of loaded files

    def set_directory(self, directory_path):
        """
        Set the directory path in the model.

        Args:
            directory_path (str): The directory path to save.
        """
        self._directory = directory_path

    def get_directory(self):
        """
        Get the currently saved directory path from the model.

        Returns:
            str: The currently saved directory path.
        """
        return self._directory

    def add_files(self, files):
        """
        Add files to the list of loaded files.

        Args:
            files (list): List of files to add.
        """
        self._loaded_files.extend(files)

    def get_files(self):
        """
        Get the list of loaded files.

        Returns:
            list: The list of loaded files.
        """
        return self._loaded_files

    def remove_files(self, files):
        """
        Remove specific files from the list of loaded files.

        Args:
            files (list): List of files to remove.
        """
        self._loaded_files = [file for file in self._loaded_files if file not in files]
