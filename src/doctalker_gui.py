import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import openai
from typing import Tuple, Dict, Union, List


class LanguageModel:

    # This is the Model class
    def __init__(self):
        self.name = None
        self.api_key = None
        self.selected_model = None
        self.temperature = None
        self.top_p = None
        self.max_tokens = None
        self.presence_penalty = None
        self.frequency_penalty = None
        # self.prompts = []
        # self.edit_log = None
        # self.submission_log = None

    def set_model_name(self, model_name):
        self.selected_model = model_name

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_model_parameters(self, param_values):
        self.temperature = param_values.get('temperature')
        self.top_p = param_values.get('top_p')
        self.max_tokens = param_values.get('max_tokens')
        self.presence_penalty = param_values.get('presence_penalty')
        self.frequency_penalty = param_values.get('frequency_penalty')
        print("Model parameters set to: ", "temp: ", self.temperature, "   top_p: ", self.top_p, "   max_tokens: ",
              self.max_tokens, "   presence_penalty: ", self.presence_penalty, "   frequency_penalty: ",
              self.frequency_penalty)


# View
class PromptsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(bg="white")  # Set the background color to white for better visibility

        # Add a simple label to the PromptsTab
        label = tk.Label(self, text="List of Prompts", bg="white")
        label.pack(pady=10)

        # Add an empty Listbox to the PromptsTab
        prompts_listbox = tk.Listbox(self, bg="white")
        prompts_listbox.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)


class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("DocTalker Chatbot")
        self.geometry("1000x770")
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

    def create_widgets(self):
        bold_font = ('Helvetica', 10, 'bold')

        # Create a ttk Notebook
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=1)

        # Create a Frame for the MainWindow tab
        prompts_tab = PromptsTab(notebook)
        notebook.add(prompts_tab, text="Chat")
        config_tab = tk.Frame(notebook)
        notebook.add(config_tab, text="Configuration Settings")

        # Create a Frame for the content area
        content_frame = tk.Frame(config_tab)
        content_frame.pack(fill=tk.BOTH, expand=1, anchor='nw')

        # Move the PanedWindow creation inside the MainWindow tab
        paned_window = tk.PanedWindow(config_tab, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=1)

        # Row 1
        row1 = tk.Frame(content_frame)
        row1.pack(fill=tk.X, padx=10, pady=5)

        # -----------------File Directory Section----------------- #
        # TODO: If the user provides a file path, the file path should be accepted and, if the user clicks Browse,the
        #  file browser should open at the selected Directory.

        row2 = tk.Frame(content_frame)
        row2.pack(fill=tk.X, padx=10, pady=3)

        content_frame.label_file_directory = tk.Label(row2, text="Files Directory Path:", font=bold_font)
        content_frame.label_file_directory.pack(side=tk.LEFT, padx=10)

        row3 = tk.Frame(content_frame)
        row3.pack(fill=tk.X, padx=10, pady=3)

        self.file_directory_entry = tk.Entry(row3)
        self.file_directory_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.file_directory_save_button = tk.Button(row3, text="Browse", font=bold_font, command=self.save_directory)
        self.file_directory_save_button.pack(side=tk.LEFT, padx=5)

        # ----------------------- Model selection ---------------------- #
        row16 = tk.Frame(content_frame)
        row16.pack(fill=tk.X, padx=10, pady=3)

        content_frame.label_model = tk.Label(row16, text="Model", font=bold_font)
        content_frame.label_model.pack(side=tk.LEFT, padx=10)

        content_frame.model_var = tk.StringVar(row16)
        content_frame.model_var.set("Select Model")  # ("Select Model")
        content_frame.model_options = ["Select Model", "gpt-4", "gpt-3.5-turbo"]
        content_frame.model_menu = tk.OptionMenu(row16, content_frame.model_var, *content_frame.model_options)
        content_frame.model_menu.pack(side=tk.LEFT, padx=10)

        # ----------------------API Key Section------------------------- #
        row14 = tk.Frame(content_frame)
        row14.pack(fill=tk.X, padx=10, pady=3)

        self.label_api_key = tk.Label(row14, text="API Key", font=bold_font)
        self.label_api_key.pack(side=tk.LEFT, padx=10)

        row15 = tk.Frame(content_frame)
        row15.pack(fill=tk.X, padx=10, pady=3)

        self.api_key_entry = tk.Entry(row15)
        self.api_key_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.api_key_save_button = tk.Button(row15, text="Save", font=bold_font, command=self.save_api_key)
        self.api_key_save_button.pack(side=tk.LEFT, padx=5)

        # ----------------------- Parameters --------------------------- #
        row17 = tk.Frame(content_frame)
        row17.pack(fill=tk.X, padx=10, pady=5)

        self.label_parameters = tk.Label(row17, text="Parameters", font=bold_font)
        self.label_parameters.pack(side=tk.LEFT, padx=10)

        row18 = tk.Frame(content_frame)
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

        row19 = tk.Frame(content_frame)
        row19.pack(fill=tk.X, padx=10, pady=3)

        # Add the top_p_entry to the parameter_entries list
        self.parameter_entries.append(self.top_p_entry)

        # -------------------------- Max_tokens ------------------------- #
        self.label_max_tokens = tk.Label(row19, text="Max_tokens (1 to 2048):")
        self.label_max_tokens.pack(side=tk.LEFT, padx=10)

        self.max_tokens_entry = tk.Entry(row19)
        self.max_tokens_entry.pack(side=tk.LEFT, padx=10)

        # Row 20
        row20 = tk.Frame(content_frame)
        row20.pack(fill=tk.X, padx=10, pady=3)

        # Add the max_tokens_entry to the parameter_entries list
        self.parameter_entries.append(self.max_tokens_entry)

        # -------------------------- Presence_penalty ------------------- #
        self.label_presence_penalty = tk.Label(row20, text="Presence_penalty (0.0 to 2.0):")
        self.label_presence_penalty.pack(side=tk.LEFT, padx=10)

        self.presence_penalty_entry = tk.Entry(row20)
        self.presence_penalty_entry.pack(side=tk.LEFT, padx=10)

        # Row 21
        row21 = tk.Frame(content_frame)
        row21.pack(fill=tk.X, padx=10, pady=3)

        # Add the presence_penalty_entry to the parameter_entries list
        self.parameter_entries.append(self.presence_penalty_entry)

        # -------------------------- Frequency_penalty ------------------ #
        self.label_frequency_penalty = tk.Label(row21, text="Frequency_penalty (0.0 to 2.0):")
        self.label_frequency_penalty.pack(side=tk.LEFT, padx=10)

        self.frequency_penalty_entry = tk.Entry(row21)
        self.frequency_penalty_entry.pack(side=tk.LEFT, padx=10)

        # Row 22
        row22 = tk.Frame(content_frame)
        row22.pack(fill=tk.X, padx=10, pady=15)

        # Add the frequency_penalty_entry to the parameter_entries list
        self.parameter_entries.append(self.frequency_penalty_entry)

        # -------------------------- Save Parameters --------------------- #
        self.parameters_save_button = tk.Button(row22, text="Save Parameters", font=bold_font,
                                                command=self.save_parameters)
        self.parameters_save_button.pack(side=tk.LEFT, padx=10)

    def save_parameters(self):
        parameters, errors = self.get_parameters()
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        success, set_errors = self.controller.set_parameters(parameters)
        if set_errors:
            messagebox.showerror("Error", "\n".join(set_errors))
            return

        for entry in self.parameter_entries:
            entry.config(bg="white")

        messagebox.showinfo("Success", "Parameters saved successfully")

    def get_parameters(self) -> Tuple[Dict[str, Union[float, int, None]], List[str]]:
        parameters: Dict[str, Union[float, int, None]] = {}
        errors = []

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
        If the directory is currently being edited, the function will disable editing and allow the user to view the directory.

        If the user is not currently editing the text of the directory and clicks the "Browse" button, the file browser will open, letting the user navigate to and select a directory. The selected directory will then be displayed in the Entry widget, and the text of the button will change to "Edit". The Entry widget will be disabled to prevent the user from manually editing the path.
        If the user is currently editing the text of the directory and clicks the "Edit" button, the Entry widget will be enabled again, allowing the user to manually edit the path, and the text of the button will change back to "Browse".

        Args:
            self: The object that this method is called on.

        Returns:
            None.
        """
        if not self.editing_directory:
            if self.file_directory_save_button["text"] == "Browse":
                directory = self.controller.browse_directory()
                if directory:
                    self.file_directory_entry.delete(0, tk.END)
                    self.file_directory_entry.insert(0, directory)
                    self.controller.set_directory(directory)
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
                self.controller.set_api_key(api_key)
                self.api_key_entry.config(state=tk.DISABLED)
                self.api_key_save_button.config(text="Edit")
                self.editing_api_key = True
        else:
            self.api_key_entry.config(state=tk.NORMAL)
            self.api_key_save_button.config(text="Save")
            self.editing_api_key = False


class LLMController:
    def __init__(self):
        self.model = LanguageModel()
        self.view = MainWindow(self)
        self.working_directory = None  # initialize the log directory to None
        self.api_key = None  # initialize the api key to None

    # Get and Set File Directory
    def browse_directory(self):
        # open a file dialog to allow the user to select a directory
        directory = tk.filedialog.askdirectory()
        if directory:
            # if a directory was selected, update the log_directory attribute
            self.working_directory = directory
            return directory
        return None

    def set_directory(self, directory):
        # set the directory attribute in the model
        print("Setting directory in the Model to " + directory)
        self.model.directory = directory
    # End of Get and Set File Directory

    # Set API Key
    def set_api_key(self, api_key):
        if self.api_key is None:
            if self.validate_api_key(api_key):
                self.model.api_key = api_key
                return True
            else:
                return False
        elif self.model.name != api_key:
            if self.validate_api_key(api_key):
                self.model.api_key = api_key
                return True
            else:
                return False
        else:
            return True

    # Validate the API Key
    def is_valid_api_key(self, api_key):
        # Makes a simple API call to determine if the API Key is valid. If the API Key is valid, return True. If the API
        # Key is invalid, return False.
        openai.api_key = api_key
        error_messages = []
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, world!"}],
                temperature=0.9, top_p=1, n=1, stream=False, max_tokens=5, presence_penalty=0, frequency_penalty=0,
                logit_bias={}, user=""
            )
            print("API Key is valid. Model Response:")
            print(response['choices'][0]['message']['content'])
        except openai.OpenAIError as e:
            print(f"Error: {e}")
            error_messages.append(str(e))
        return error_messages

    def validate_api_key(self, api_key):
        # Validate the API Key. If the API Key is valid, set it in the model and return True. If the API Key is invalid,
        # return False.
        error_messages = self.is_valid_api_key(api_key)
        if error_messages:
            messagebox.showerror("Invalid API Key:", "Invalid API Key entered.\n" + "\n".join(error_messages))
            return False
        else:
            return True
    # End of Validate the API Key

    # Validate parameters. If the parameters are valid, set them in the model
    def set_parameters(self, parameters):
        # Sets the parameters in the model if they are valid. Returns True if the parameters are valid, False otherwise.
        errors = []

        for key, value in parameters.items():
            if value is None:
                errors.append(f"Invalid {key} value")

        if errors:
            return False, errors

        self.model.set_model_parameters(parameters)
        return True, None

    # End of Validate parameters.


# Main function
def main():
    controller = LLMController()
    controller.view.mainloop()


if __name__ == "__main__":
    main()
