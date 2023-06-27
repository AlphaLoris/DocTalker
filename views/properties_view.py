import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.open_ai_capabilities import populate_model_list, get_api_key, is_valid_api_key_model


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="light grey", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class PropertiesView:

    def __init__(self, application_controller, parent, context_windows):
        self.browse_button = None
        self.properties_controller = None
        self.application_controller = application_controller
        self.parent = parent
        self.context_windows = context_windows
        self.properties = {}
        self.submit_button_frame = None
        self.submit_button = None
        self.model_parameters_frame = None
        self.top = None
        self.label_working_files_path = None
        self.working_files_path_entry = None
        self.stream_frame = None
        self.stream_var = None
        self.stream_label = None
        self.stream_true_button = None
        self.stream_false_button = None
        self.token_count_label = None
        self.token_count_value = None
        self.context_length_label = None
        self.context_length_value = None
        self.context_length = None
        self.user_label = None
        self.user_entry = None
        self.logit_bias_label = None
        self.logit_bias_entry = None
        self.frequency_penalty_label = None
        self.frequency_penalty_entry = None
        self.presence_penalty_label = None
        self.presence_penalty_entry = None
        self.max_tokens_label = None
        self.max_tokens_entry = None
        self.stop_label = None
        self.stop_entry = None
        self.n_label = None
        self.top_p_label = None
        self.n_entry = None
        self.temperature_label = None
        self.temperature_entry = None
        self.label_api_key = None
        self.api_key_label = None
        self.edit_api_key_button = None
        self.top_p_entry = None
        self.api_key = ""
        self.api_key_entry = None
        self.refresh_button = None
        self.model_menu = None
        self.model_var = None
        self.token_count = None
        self.parameters_frame = None

    def on_model_change(self, *args):
        selected_model = self.model_menu.get()
        print(f"Selected model: {selected_model}")
        if selected_model != "Select Model":
            print("Model has been selected. Displaying model parameters.")
            self.model_parameters_frame.grid()
            self.submit_button_frame.grid()
            self.model_parameters_frame.update_idletasks()
            self.submit_button_frame.update_idletasks()
        else:
            print("Model has not been selected. Hiding model parameters.")
            self.model_parameters_frame.grid_forget()
            self.submit_button_frame.grid_forget()

    def center_window(self, window, width=300, height=200):
        # Gets the requested windows width and height
        window_width = width
        window_height = height

        # Gets both half the screen width/height and window width/height
        position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(window.winfo_screenheight() / 2 - window_height / 2)

        # Positions the window in the center of the page.
        window.geometry("+{}+{}".format(position_right, position_down))

    def get_properties_from_user(self):
        self.top = tk.Toplevel(self.parent)
        self.top.title("Enter properties")
        self.top.grab_set()  # Make the properties window modal
        self.center_window(self.top, width=400, height=300)  # You can adjust the width and height

        # Parameters frame
        self.parameters_frame = tk.Frame(self.top)
        self.parameters_frame.grid(row=0, column=0, rowspan=3, columnspan=6, sticky="w")
        self.parameters_frame.columnconfigure(0, weight=0, minsize=5)
        self.parameters_frame.columnconfigure(1, weight=0, minsize=5)
        self.parameters_frame.columnconfigure(2, weight=0, minsize=5)
        self.parameters_frame.columnconfigure(3, weight=0, minsize=5)
        self.parameters_frame.columnconfigure(4, weight=0, minsize=5)
        self.parameters_frame.columnconfigure(5, weight=1)

        # working_files_path
        self.browse_button = tk.Button(self.parameters_frame, text="Browse", width=15, command=self.get_files_directory)
        self.browse_button.grid(row=0, column=0, padx=5, pady=5)
        self.working_files_path_entry = tk.Entry(self.parameters_frame, width=100)
        self.working_files_path_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=4, sticky="w")
        self.label_working_files_path = tk.Label(self.parameters_frame, text="Working files path", width=15, anchor="w")
        self.label_working_files_path.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        working_files_path_tooltip_text = "The working file path is the path to the folder where the working files\n" \
                                          "will be stored."
        ToolTip(self.label_working_files_path, working_files_path_tooltip_text)

        # API Key
        self.edit_api_key_button = tk.Button(self.parameters_frame, text="Edit API Key", width=15,
                                             command=self.edit_api_key)
        print("API Key entered in properties_view: " + self.api_key)
        self.edit_api_key_button.grid(row=1, column=0, padx=5, pady=5)
        self.api_key_entry = tk.Entry(self.parameters_frame, width=100, state='readonly')
        self.api_key_entry.grid(row=1, column=1, padx=10)
        self.api_key_entry.insert(0, self.api_key)
        self.label_api_key = tk.Label(self.parameters_frame, text="API Key", width=15, justify="left", anchor="w")
        self.label_api_key.grid(row=1, column=3, padx=3, sticky="w")
        api_key_tooltip_text = "The API Key is the code necessary to access the API of the LLM.\n " \
                               "The API Key For access to the OpenAI Chat Completion API is available on\n " \
                               "your account page on the OpenAI website at this URL:\n\n" \
                               "https://platform.openai.com/account/api-keys\n\n" \
                               "(You may have to associate a payment method with your account to generate an API Key.)"
        ToolTip(self.label_api_key, api_key_tooltip_text)

        # Model
        self.model_var = tk.StringVar(self.parameters_frame)
        self.refresh_button = tk.Button(self.parameters_frame, text="Refresh Models", width=12,
                                        command=lambda: self.refresh_model_list(self.context_windows))
        self.refresh_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.model_var.set("Select Model")
        self.model_menu = ttk.Combobox(self.parameters_frame, textvariable=self.model_var)
        self.model_menu.set("Select Model")  # default value
        self.model_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w", columnspan=1)
        self.model_parameters_frame = tk.Frame(self.top)
        self.model_parameters_frame.grid(row=3, column=0, rowspan=6, columnspan=4, sticky="w")
        self.model_parameters_frame.grid_forget()
        self.model_menu.bind("<<ComboboxSelected>>", self.on_model_change)

        # Temperature
        self.temperature_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.temperature_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nswe")
        self.temperature_entry.insert(0, "0.7")
        self.temperature_label = tk.Label(self.model_parameters_frame, text="temperature (0-2)", width=20, anchor="w")
        self.temperature_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        temperature_tooltip_text = "The temperature parameter controls the randomness of the model's response\n" \
                                   "by controlling the likelihood that the model will return the most probable \n" \
                                   "next token (word) versus a less probable next token. The higher the" \
                                   " temperature, \nthe more random the choice of next token."
        ToolTip(self.temperature_label, temperature_tooltip_text)

        # Top_p
        self.top_p_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.top_p_entry.grid(row=4, column=0, padx=10, pady=5, sticky="nswe")
        self.top_p_entry.insert(0, "1.0")
        self.top_p_label = tk.Label(self.model_parameters_frame, text="top_p (0-1)", width=20, anchor="w")
        self.top_p_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        top_p_tooltip_text = "The top_p parameter also controls the randomness of the model's response \n" \
                             "by limiting the set of tokens that the model is allowed to select from when\n" \
                             "choosing the next token.  If top_p is set to 0.1, the model must choose the\n" \
                             "next token (word) from the top 10% most probable tokens. The higher the\n" \
                             "top_p value,the larger the set of tokens the model has to choose from."
        ToolTip(self.top_p_label, top_p_tooltip_text)

        # n
        self.n_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.n_entry.grid(row=5, column=0, padx=10, pady=5, sticky="nswe")
        self.n_entry.insert(0, "1")
        self.n_label = tk.Label(self.model_parameters_frame, text="n (1-4)", width=20, anchor="w")
        self.n_label.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        n_label_tooltip_text = "The n parameter determines the number of different completions the model will \n" \
                               "return.  If n is set to 3, the model will return three completions."
        ToolTip(self.n_label, n_label_tooltip_text)

        # Stream frame
        self.stream_frame = tk.Frame(self.model_parameters_frame)
        self.stream_frame.grid(row=6, column=0, columnspan=2, sticky="w")

        # Stream variable, label and radio buttons within stream frame
        self.stream_var = tk.StringVar(value="False")  # default value
        self.stream_label = tk.Label(self.stream_frame, text="stream (Off/On)", width=20, anchor="w")
        self.stream_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.stream_false_button = tk.Radiobutton(self.stream_frame, text="Off", variable=self.stream_var,
                                                  value="False")
        self.stream_false_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.stream_true_button = tk.Radiobutton(self.stream_frame, text="On", variable=self.stream_var, value="True")
        self.stream_true_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Tooltip
        stream_label_tooltip_text = "The stream parameter determines whether the model will return its response as \n" \
                                    "a stream as it is generated or as a single response when the model has finished."
        ToolTip(self.stream_label, stream_label_tooltip_text)

        # stop
        self.stop_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.stop_entry.grid(row=7, column=0, padx=10, pady=5, sticky="nswe")
        self.stop_entry.insert(0, "")
        self.stop_label = tk.Label(self.model_parameters_frame, text="stop (text string(s))", width=20, anchor="w")
        self.stop_label.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        stop_label_tooltip_text = 'The stop parameter determines when the model will stop generating text. If the \n' \
                                  'model generates one of the strings (you can provide up to four strings) provided, it \n' \
                                  'will stop generating text and return the result, which will not include the stop \n' \
                                  'string. The strings should be enclosed in quotation marks and separated by a comma\n' \
                                  'and a space. For example, "11.", "Hello Michael", "Go home!"'
        ToolTip(self.stop_label, stop_label_tooltip_text)

        # max_tokens
        self.max_tokens_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.max_tokens_entry.grid(row=8, column=0, padx=10, pady=5, sticky="nswe")
        self.max_tokens_entry.insert(0, "")
        self.max_tokens_label = tk.Label(self.model_parameters_frame, text="max_tokens (1-?)", width=20, anchor="w")
        self.max_tokens_label.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        max_tokens_label_tooltip_text = "The max_tokens parameter specifies the maximum number of tokens the model is\n" \
                                        "to generate in the chat completion. The total length of input tokens and\n" \
                                        "generated tokens is limited by the model's context window. For GPT-4,\n" \
                                        "the context length is 8192 tokens, So the max_tokens value is limited to\n" \
                                        "the context length - prompt message tokens, but the value you assign can\n" \
                                        "be less than that."
        ToolTip(self.max_tokens_label, max_tokens_label_tooltip_text)

        # presence_penalty
        self.presence_penalty_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.presence_penalty_entry.grid(row=3, column=3, padx=5, pady=5, sticky="nswe")
        self.presence_penalty_entry.insert(0, "")
        self.presence_penalty_label = tk.Label(self.model_parameters_frame, text="presence_penalty (-2.0 to 2.0)",
                                               width=24, anchor="w")
        self.presence_penalty_label.grid(row=3, column=4, padx=5, pady=5, sticky="w")
        presence_penalty_label_tooltip_text = "Presence_penalty controls the model's likelihood of using words that\n" \
                                              "already occur in its output again. Positive values penalize new tokens \n" \
                                              "based on whether they appear in the text so far, increasing the model's\n" \
                                              "likelihood to talk about new topics."
        ToolTip(self.presence_penalty_label, presence_penalty_label_tooltip_text)

        # frequency_penalty
        self.frequency_penalty_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.frequency_penalty_entry.grid(row=4, column=3, padx=5, pady=5, sticky="nswe")
        self.frequency_penalty_entry.insert(0, "")
        self.frequency_penalty_label = tk.Label(self.model_parameters_frame, text="frequency_penalty (-2.0 to 2.0)",
                                                width=24, anchor="w")
        self.frequency_penalty_label.grid(row=4, column=4, padx=5, pady=5, sticky="w")
        frequency_penalty_label_tooltip_text = "Frequency_penalty is a number between -2.0 and 2.0 that defaults to 0.\n " \
                                               "Positive values penalize new tokens based on their existing frequency in\n" \
                                               "the text so far, decreasing the model's likelihood to repeat the same \n" \
                                               "line verbatim."
        ToolTip(self.frequency_penalty_label, frequency_penalty_label_tooltip_text)

        # logit_bias
        self.logit_bias_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.logit_bias_entry.grid(row=5, column=3, padx=5, pady=5, sticky="nswe")
        self.logit_bias_entry.insert(0, "")
        self.logit_bias_label = tk.Label(self.model_parameters_frame, text="logit_bias (JSON)", width=16,
                                         anchor="w")
        self.logit_bias_label.grid(row=5, column=4, padx=5, pady=5, sticky="w")
        logit_bias_label_tooltip_text = "The logit_bias parameter is a JSON object that allows you to adjust the\n" \
                                        "likelihood of the model generating certain words. The keys are tokens and\n" \
                                        "the values are bias values. Positive bias values increase the likelihood of\n" \
                                        "the model generating the associated word, while negative values decrease the\n" \
                                        "likelihood. The bias values are on a log scale, so a value of 1.0 increases\n" \
                                        "the likelihood by 10x, and a value of -1.0 decreases the likelihood by 10x."
        ToolTip(self.logit_bias_label, logit_bias_label_tooltip_text)

        # user
        self.user_entry = tk.Entry(self.model_parameters_frame, width=15)
        self.user_entry.grid(row=6, column=3, padx=5, pady=5, sticky="nswe")
        self.user_entry.insert(0, "")
        self.user_label = tk.Label(self.model_parameters_frame, text="user [user ID]", width=16,
                                   anchor="w")
        self.user_label.grid(row=6, column=4, padx=5, pady=5, sticky="w")
        user_label_tooltip_text = "The user parameter is a string that allows you to associate a prompt with a\n" \
                                  "specific user. This is intended to be used for tracking which user within an\n" \
                                  " organization submitted which prompts."
        ToolTip(self.user_label, user_label_tooltip_text)

        self.submit_button_frame = tk.Frame(self.top)
        self.submit_button_frame.grid(row=9, column=0, rowspan=6, columnspan=1, sticky="w")
        self.submit_button_frame.grid_forget()
        self.submit_button = tk.Button(self.submit_button_frame, text="Submit", width=15,
                                       command=self.properties_controller.handle_submit)
        self.submit_button.grid(row=9, column=0, padx=5, pady=5, sticky="w")

    def set_properties_controller(self, properties_controller):
        self.properties_controller = properties_controller
        print("PropertiesView set properties_controller")

    def configure_submit_button_command(self):
        print("Configuring the submit_button_command")
        self.submit_button.configure(command=self.properties_controller.handle_submit)


    # def configure_edit_api_key_button_command(self):
    #    print("Configuring the edit_api_key_button_command")
    #     self.edit_api_key_button.config(command=self.edit_api_key)

    def get_properties(self):
        self.properties['working_files_path'] = self.working_files_path_entry.get()
        self.properties['api_key'] = self.api_key_entry.get()
        self.properties['model'] = self.model_var.get()
        self.properties['temperature'] = self.temperature_entry.get()
        self.properties['top_p'] = self.top_p_entry.get()
        self.properties['n'] = self.n_entry.get()
        self.properties['stream'] = self.stream_var.get()
        self.properties['stop'] = self.stop_entry.get()
        self.properties['max_tokens'] = self.max_tokens_entry.get()
        self.properties['presence_penalty'] = self.presence_penalty_entry.get()
        self.properties['frequency_penalty'] = self.frequency_penalty_entry.get()
        self.properties['logit_bias'] = self.logit_bias_entry.get()
        self.properties['user'] = self.user_entry.get()
        return self.properties

    def close_window(self):
        self.top.destroy()

    def show_error_message(self, errors):
        error_message = "The following errors occurred:\n" + errors
        messagebox.showerror("Invalid values", error_message)

    def refresh_model_list(self, context_windows, api_key):
        # api_key = self.properties_controller.get_property('api_key')
        print("API key retrieved from properties model for use in refreshing model list: ", api_key)
        model_list = populate_model_list(context_windows, api_key)
        print("Updating model list: " + str(model_list))
        self.model_menu['values'] = ["Select Model"] + model_list

    def get_files_directory(self):
        file_directory = filedialog.askdirectory()
        self.working_files_path_entry.delete(0, 'end')
        self.working_files_path_entry.insert(0, file_directory)

    def edit_api_key(self):
        print("edit_api_key called in properties_view")
        new_api_key = get_api_key(self.top)

        # Check if the user has cancelled the input (assuming get_api_key returns None or an empty string in that case)
        if not new_api_key:
            # Optionally, you can log or show a message that the user cancelled the input.
            print("User cancelled the input.")
            return  # Exit the method early as there's nothing to process.

        print("New API key passed to edit_api_key in properties_view: ", new_api_key)

        self.api_key_entry.config(state='normal')  # Temporarily make the field editable
        self.api_key_entry.delete(0, 'end')
        self.api_key_entry.insert(0, new_api_key)
        self.api_key_entry.config(state='readonly')  # Make the field read-only again

        # Validate API key
        test_model = "gpt-3.5-turbo"
        try:
            is_valid_api_key_model(new_api_key, test_model)
        except Exception as e:
            messagebox.showerror("Invalid API key", "The API key you entered is invalid. Please try again.")
        else:
            # Only refresh the model list if the API key is valid
            self.properties_controller.set_property('api_key', new_api_key)
            self.refresh_model_list(self.context_windows, new_api_key)
