import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Tuple, Dict, Union, List


class LLMView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.llm_controller = controller
        self.parameter_entries = []
        self.editing_parameters = False
        self.editing_name = False
        self.editing_directory = False
        self.editing_description = False
        self.editing_api_key = False
        self.editing_parameters = False
        self.create_widgets()
        self.parameters_save_button = None
        self.frequency_penalty_entry = None
        self.label_frequency_penalty = None
        self.presence_penalty_entry = None
        self.label_presence_penalty = None
        self.max_tokens_entry = None
        self.label_max_tokens = None
        self.top_p_entry = None
        self.label_top_p = None
        self.temperature_entry = None
        self.label_temperature = None
        self.label_parameters = None
        self.api_key_save_button = None
        self.api_key_entry = None
        self.label_api_key = None
        self.name_save_button = None
        self.name_entry = None
        self.label_name = None
        self.file_directory_save_button = None
        self.file_directory_entry = None
        self.label_file_directory = None
        self.model_options = None
        self.model_var = None
        self.label_model = None
        self.model_menu = None

    def create_widgets(self):
        bold_font = ('Helvetica', 10, 'bold')

        # Row 1
        row1 = tk.Frame(self)
        row1.pack(fill=tk.X, padx=10, pady=5)

        # -----------------File Directory Section----------------- #
        # TODO: If the user provides a file path, the file path should be accepted and, if the user clicks Browse,the
        #  file browser should open at the selected Directory.

        row2 = tk.Frame(self)
        row2.pack(fill=tk.X, padx=10, pady=3)

        self.label_file_directory = tk.Label(row2, text="Application Files Directory Path:", font=bold_font)
        self.label_file_directory.pack(side=tk.LEFT, padx=10)

        row3 = tk.Frame(self)
        row3.pack(fill=tk.X, padx=10, pady=3)

        self.file_directory_entry = tk.Entry(row3)
        self.file_directory_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.file_directory_save_button = tk.Button(row3, text="Browse", font=bold_font, command=self.save_directory)
        self.file_directory_save_button.pack(side=tk.LEFT, padx=5)

        # ----------------------- Model selection ---------------------- #
        row16 = tk.Frame(self)
        row16.pack(fill=tk.X, padx=10, pady=3)

        self.label_model = tk.Label(row16, text="Model", font=bold_font)
        self.label_model.pack(side=tk.LEFT, padx=10)

        self.model_var = tk.StringVar(row16)
        self.model_var.set("Select Model")  # ("Select Model")
        self.model_options = ["Select Model", "gpt-4", "gpt-3.5-turbo"]
        self.model_menu = tk.OptionMenu(row16, self.model_var, *self.model_options)
        self.model_menu.pack(side=tk.LEFT, padx=10)

        # ----------------------API Key Section------------------------- #
        row14 = tk.Frame(self)
        row14.pack(fill=tk.X, padx=10, pady=3)

        self.label_api_key = tk.Label(row14, text="API Key", font=bold_font)
        self.label_api_key.pack(side=tk.LEFT, padx=10)

        row15 = tk.Frame(self)
        row15.pack(fill=tk.X, padx=10, pady=3)

        self.api_key_entry = tk.Entry(row15)
        self.api_key_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.api_key_save_button = tk.Button(row15, text="Save", font=bold_font, command=self.save_api_key)
        self.api_key_save_button.pack(side=tk.LEFT, padx=5)

        # ----------------------- Parameters --------------------------- #
        row17 = tk.Frame(self)
        row17.pack(fill=tk.X, padx=10, pady=5)

        self.label_parameters = tk.Label(row17, text="Parameters", font=bold_font)
        self.label_parameters.pack(side=tk.LEFT, padx=10)

        row18 = tk.Frame(self)
        row18.pack(fill=tk.X, padx=10, pady=3)

        # -------------------------- Temperature ----------------------- #
        self.label_temperature = tk.Label(row18, text="Temperature (0.0 to 1.0):")
        self.label_temperature.pack(side=tk.LEFT, padx=10)

        self.temperature_entry = tk.Entry(row18)
        self.temperature_entry.pack(side=tk.LEFT, padx=10)

        # Add the temperature_entry to the parameter_entries list
        self.parameter_entries.append(self.temperature_entry)

        # -------------------------- Top_p ----------------------------- #
        self.label_top_p = tk.Label(row18, text="Top_p (0.0 to 1.0):")
        self.label_top_p.pack(side=tk.LEFT, padx=10)

        self.top_p_entry = tk.Entry(row18)
        self.top_p_entry.pack(side=tk.LEFT, padx=20)

        row19 = tk.Frame(self)
        row19.pack(fill=tk.X, padx=10, pady=3)

        # Add the top_p_entry to the parameter_entries list
        self.parameter_entries.append(self.top_p_entry)

        # -------------------------- Max_tokens ------------------------- #
        self.label_max_tokens = tk.Label(row19, text="Max_tokens (1 to 2048):")
        self.label_max_tokens.pack(side=tk.LEFT, padx=10)

        self.max_tokens_entry = tk.Entry(row19)
        self.max_tokens_entry.pack(side=tk.LEFT, padx=10)

        # Row 20
        row20 = tk.Frame(self)
        row20.pack(fill=tk.X, padx=10, pady=3)

        # Add the max_tokens_entry to the parameter_entries list
        self.parameter_entries.append(self.max_tokens_entry)

        # -------------------------- Presence_penalty ------------------- #
        self.label_presence_penalty = tk.Label(row20, text="Presence_penalty (0.0 to 2.0):")
        self.label_presence_penalty.pack(side=tk.LEFT, padx=10)

        self.presence_penalty_entry = tk.Entry(row20)
        self.presence_penalty_entry.pack(side=tk.LEFT, padx=10)

        # Row 21
        row21 = tk.Frame(self)
        row21.pack(fill=tk.X, padx=10, pady=3)

        # Add the presence_penalty_entry to the parameter_entries list
        self.parameter_entries.append(self.presence_penalty_entry)

        # -------------------------- Frequency_penalty ------------------ #
        self.label_frequency_penalty = tk.Label(row21, text="Frequency_penalty (0.0 to 2.0):")
        self.label_frequency_penalty.pack(side=tk.LEFT, padx=10)

        self.frequency_penalty_entry = tk.Entry(row21)
        self.frequency_penalty_entry.pack(side=tk.LEFT, padx=10)

        # Row 22
        row22 = tk.Frame(self)
        row22.pack(fill=tk.X, padx=10, pady=15)

        # Add the frequency_penalty_entry to the parameter_entries list
        self.parameter_entries.append(self.frequency_penalty_entry)

        # -------------------------- Save Parameters --------------------- #
        self.parameters_save_button = tk.Button(row22, text="Save Parameters", font=bold_font,
                                                command=self.save_parameters)
        self.parameters_save_button.pack(side=tk.LEFT, padx=10)

    def save_parameters(self):
        """
        Saves the parameters from the UI to the model.
        Raises an exception if the parameters are invalid or if there is an error saving the parameters to the model.
        """
        parameters, errors = self.get_parameters()
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        success, set_errors = self.llm_controller.set_parameters(parameters)
        if set_errors:
            messagebox.showerror("Error", "\n".join(set_errors))
            return

        for entry in self.parameter_entries:
            entry.config(bg="white")

        messagebox.showinfo("Success", "Parameters saved successfully")

    def get_parameters(self) -> Tuple[Dict[str, Union[float, int, None]], List[str]]:
        parameters: Dict[str, Union[float, int, None]] = {}
        errors = []

        """
        This method gets the parameter values from the corresponding UI elements and validate that they fall within the
        valid range for each parameter.
        Returns:
            A tuple of the following:
            - A dictionary of parameter values.
            - A list of error messages.
        """

        def validate_float(value, min_value, max_value):
            try:
                value = float(value)
                if min_value <= value <= max_value:
                    return value
                else:
                    raise ValueError
            except ValueError:
                return None

        parameters['temperature'] = validate_float(self.temperature_entry.get(), 0.0, 1.0)
        if parameters['temperature'] is None:
            errors.append("Invalid temperature value. Must be between 0.0 and 1.0.")

        parameters['top_p'] = validate_float(self.top_p_entry.get(), 0.0, 1.0)
        if parameters['top_p'] is None:
            errors.append("Invalid top_p value. Must be between 0.0 and 1.0.")

        try:
            parameters['max_tokens'] = int(self.max_tokens_entry.get())
            if not 1 <= parameters['max_tokens'] <= 2048:
                raise ValueError
        except ValueError:
            errors.append("Invalid max_tokens value. Must be between 1 and 2048.")
            parameters['max_tokens'] = None

        parameters['presence_penalty'] = validate_float(self.presence_penalty_entry.get(), 0.0, 2.0)
        if parameters['presence_penalty'] is None:
            errors.append("Invalid presence_penalty value. Must be between 0.0 and 2.0.")

        parameters['frequency_penalty'] = validate_float(self.frequency_penalty_entry.get(), 0.0, 2.0)
        if parameters['frequency_penalty'] is None:
            errors.append("Invalid frequency_penalty value. Must be between 0.0 and 2.0.")

        return parameters, errors

    def save_directory(self):
        """
        Save the directory value currently selected in the UI to the model.
        If the directory value is not currently being edited, the function will browse for a new directory.
        If the directory is currently being edited, the function will disable editing and allow the user to view the
        directory.

        Args:
            self: The object that this method is called on.

        Returns:
            None.
        """
        if not self.editing_directory:
            if self.file_directory_save_button["text"] == "Browse":
                directory = self.llm_controller.browse_directory()
                if directory:
                    self.file_directory_entry.delete(0, tk.END)
                    self.file_directory_entry.insert(0, directory)
                    self.llm_controller.set_directory(directory)
                    self.file_directory_entry.config(state=tk.DISABLED)
                    self.file_directory_save_button.config(text="Edit")
                    self.editing_directory = True
            else:
                self.file_directory_entry.config(state=tk.NORMAL)
                self.file_directory_save_button.config(text="Browse")
                self.editing_directory = False

    def save_api_key(self):
        if not self.editing_api_key:
            api_key = self.api_key_entry.get()
            if api_key:
                self.llm_controller.set_api_key(api_key)
                self.api_key_entry.config(state=tk.DISABLED)
                self.api_key_save_button.config(text="Edit")
                self.editing_api_key = True
        else:
            self.api_key_entry.config(state=tk.NORMAL)
            self.api_key_save_button.config(text="Save")
            self.editing_api_key = False
