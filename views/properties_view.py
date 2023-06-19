import tkinter as tk
from tkinter import ttk
from utils.open_ai_capabilities import populate_model_list, get_api_key


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
    def __init__(self, parent, context_windows):
        self.model_parameters_frame = None
        self.top = None
        self.label_working_files_path = None
        self.working_files_path_entry = None
        self.stream_label = None
        self.stream_entry = None
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
        self.edit_button = None
        self.top_p_entry = None
        self.api_key = ""
        self.context_windows = context_windows
        self.api_key_entry = None
        self.refresh_button = None
        self.model_menu = None
        self.model_var = None
        self.token_count = None
        self.parameters_frame = None
        self.parent = parent

    def get_properties_from_user(self):
        properties = {}
        self.top = tk.Toplevel(self.parent)
        self.top.title("Enter properties")
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
        self.working_files_path_entry = tk.Entry(self.parameters_frame, width=120)
        self.working_files_path_entry.grid(row=0, column=0, padx=10, pady=5, columnspan=4, sticky="w")
        self.label_working_files_path = tk.Label(self.parameters_frame, text="Working file path", width=15, anchor="w")
        self.label_working_files_path.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        working_files_path_tooltip_text = "The working file path is the path to the folder where the working files\n" \
                                          "will be stored.\n"
        ToolTip(self.label_working_files_path, working_files_path_tooltip_text)

        # API Key
        self.edit_button = tk.Button(self.parameters_frame, text="Edit API Key", width=15, command=self.edit_api_key)
        self.edit_button.grid(row=1, column=0, padx=5, pady=5)
        self.api_key_entry = tk.Entry(self.parameters_frame, width=100)
        self.api_key_entry.grid(row=1, column=1, padx=5)
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
                                        command=lambda: self.refresh_model_list(self.context_windows, self.api_key))
        self.refresh_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.model_var.set("Select Model")
        self.model_menu = ttk.Combobox(self.parameters_frame, textvariable=self.model_var)
        self.model_menu.set("Select Model")  # default value
        self.model_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w", columnspan=1)

        self.model_parameters_frame = tk.Frame(self.top)
        self.model_parameters_frame.grid(row=3, column=0, rowspan=6, columnspan=4, sticky="w")

        # Temperature
        self.temperature_entry = tk.Entry(self.model_parameters_frame, width=10)
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
        self.top_p_entry = tk.Entry(self.model_parameters_frame, width=10)
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
        self.n_entry = tk.Entry(self.model_parameters_frame, width=10)
        self.n_entry.grid(row=5, column=0, padx=10, pady=5, sticky="nswe")
        self.n_entry.insert(0, "1")
        self.n_label = tk.Label(self.model_parameters_frame, text="n (1-4)", width=20, anchor="w")
        self.n_label.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        n_label_tooltip_text = "The n parameter determines the number of different completions the model will \n" \
                               "return.  If n is set to 3, the model will return three completions."
        ToolTip(self.n_label, n_label_tooltip_text)

        # Stream
        self.stream_entry = tk.Entry(self.model_parameters_frame, width=10)
        self.stream_entry.grid(row=6, column=0, padx=10, pady=5, sticky="nswe")
        self.stream_entry.insert(0, "1")
        self.stream_label = tk.Label(self.model_parameters_frame, text="stream (True or False)", width=20, anchor="w")
        self.stream_label.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        stream_label_tooltip_text = "The stream parameter determines whether the model will return its response as \n" \
                                    "a stream as it is generated or as a single response when the model has finished."
        ToolTip(self.n_label, stream_label_tooltip_text)

        # stop
        self.stop_entry = tk.Entry(self.model_parameters_frame, width=10)
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
        self.max_tokens_entry = tk.Entry(self.model_parameters_frame, width=10)
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
        self.presence_penalty_entry = tk.Entry(self.model_parameters_frame, width=10)
        self.presence_penalty_entry.grid(row=3, column=3, padx=5, pady=5, sticky="nswe")
        self.presence_penalty_entry.insert(0, "")
        self.presence_penalty_label = tk.Label(self.model_parameters_frame, text="presence_penalty (-2.0 to 2.0)", width=24,
                                               anchor="w")
        self.presence_penalty_label.grid(row=3, column=4, padx=5, pady=5, sticky="w")
        presence_penalty_label_tooltip_text = "Presence_penalty controls the model's likelihood of using words that\n" \
                                              "already occur in its output again. Positive values penalize new tokens \n" \
                                              "based on whether they appear in the text so far, increasing the model's\n" \
                                              "likelihood to talk about new topics."
        ToolTip(self.presence_penalty_label, presence_penalty_label_tooltip_text)

        # frequency_penalty
        self.frequency_penalty_entry = tk.Entry(self.model_parameters_frame, width=10)
        self.frequency_penalty_entry.grid(row=4, column=3, padx=5, pady=5, sticky="nswe")
        self.frequency_penalty_entry.insert(0, "")
        self.frequency_penalty_label = tk.Label(self.model_parameters_frame, text="frequency_penalty (-2.0 to 2.0)", width=24,
                                                anchor="w")
        self.frequency_penalty_label.grid(row=4, column=4, padx=5, pady=5, sticky="w")
        frequency_penalty_label_tooltip_text = "Frequency_penalty is a number between -2.0 and 2.0 that defaults to 0.\n " \
                                               "Positive values penalize new tokens based on their existing frequency in\n" \
                                               "the text so far, decreasing the model's likelihood to repeat the same \n" \
                                               "line verbatim."
        ToolTip(self.frequency_penalty_label, frequency_penalty_label_tooltip_text)

        # logit_bias
        self.logit_bias_entry = tk.Entry(self.model_parameters_frame, width=10)
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
        self.user_entry = tk.Entry(self.model_parameters_frame, width=10)
        self.user_entry.grid(row=6, column=3, padx=5, pady=5, sticky="nswe")
        self.user_entry.insert(0, "")
        self.user_label = tk.Label(self.model_parameters_frame, text="user [user ID]", width=16,
                                   anchor="w")
        self.user_label.grid(row=6, column=4, padx=5, pady=5, sticky="w")
        user_label_tooltip_text = "The user parameter is a string that allows you to associate a prompt with a\n" \
                                  "specific user. This is intended to be used for tracking which user within an\n" \
                                  " organization submitted which prompts."
        ToolTip(self.user_label, user_label_tooltip_text)

        def submit():
            properties['working_files_path'] = self.working_files_path_entry.get()
            properties['api_key'] = self.api_key_entry.get()
            properties['temperature'] = self.temperature_entry.get()
            properties['top_p'] = self.top_p_entry.get()
            properties['n'] = self.n_entry.get()
            properties['stream'] = self.stream_entry.get()
            properties['stop'] = self.stop_entry.get()
            properties['max_tokens'] = self.max_tokens_entry.get()
            properties['presence_penalty'] = self.presence_penalty_entry.get()
            properties['frequency_penalty'] = self.frequency_penalty_entry.get()
            properties['logit_bias'] = self.logit_bias_entry.get()
            properties['user'] = self.user_entry.get()
            self.top.destroy()

    def refresh_model_list(self, context_windows, api_key):
        model_list = populate_model_list(context_windows, api_key)
        print("Updating model list: " + str(model_list))
        self.model_menu['values'] = ["Select Model"] + model_list

    def edit_api_key(self):
        # Here is where you'd put the logic to edit the API Key
        new_api_key = get_api_key(self.top)
        if new_api_key:
            self.api_key_entry.delete(0, 'end')
            self.api_key_entry.insert(0, new_api_key)
            self.refresh_model_list(self.context_windows,
                                    new_api_key)  # Refresh the model list after updating the API key

        """
        top = tk.Toplevel(self.parent)
        top.title("Enter properties")
        working_files_path_label = tk.Label(top, text="Working Files Path: ")
        working_files_path_label.pack()
        working_files_path_entry = tk.Entry(top)
        working_files_path_entry.pack()
        api_key_label = tk.Label(top, text="API Key: ")
        api_key_label.pack()
        api_key_entry = tk.Entry(top)
        api_key_entry.pack()
        temperature_label = tk.Label(top, text="temperature: ")
        temperature_label.pack()
        temperature_entry = tk.Entry(top)
        temperature_entry.pack()
        top_p_label = tk.Label(top, text="top_p: ")
        top_p_label.pack()
        top_p_entry = tk.Entry(top)
        top_p_entry.pack()
        n_label = tk.Label(top, text="n: ")
        n_label.pack()
        n_entry = tk.Entry(top)
        n_entry.pack()
        stream_label = tk.Label(top, text="stream: ")
        stream_label.pack()
        stream_entry = tk.Entry(top)
        stream_entry.pack()
        stop_label = tk.Label(top, text="stop: ")
        stop_label.pack()
        stop_entry = tk.Entry(top)
        stop_entry.pack()
        max_tokens_label = tk.Label(top, text="max_tokens: ")
        max_tokens_label.pack()
        max_tokens_entry = tk.Entry(top)
        max_tokens_entry.pack()
        presence_penalty_label = tk.Label(top, text="presence_penalty: ")
        presence_penalty_label.pack()
        presence_penalty_entry = tk.Entry(top)
        presence_penalty_entry.pack()
        frequency_penalty_label = tk.Label(top, text="frequency_penalty: ")
        frequency_penalty_label.pack()
        frequency_penalty_entry = tk.Entry(top)
        frequency_penalty_entry.pack()
        logit_bias_label = tk.Label(top, text="logit_bias: ")
        logit_bias_label.pack()
        logit_bias_entry = tk.Entry(top)
        logit_bias_entry.pack()
        user_label = tk.Label(top, text="user: ")
        user_label.pack()
        user_entry = tk.Entry(top)
        user_entry.pack()
        submit_button = tk.Button(top, text="Submit", command=submit)
        submit_button.pack()
        self.parent.wait_window(top)

        return properties
        """
