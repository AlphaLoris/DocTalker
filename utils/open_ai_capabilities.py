import tkinter as tk
from tkinter import simpledialog, messagebox
import tiktoken
import openai
import requests
import os


# Function to determine the number of tokens in a message
def num_tokens_from_messages(messages, model):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        print("counting tokens for model", model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See
         https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to
          tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# The send_request function submits the prompt to the Chat Completion API
def send_request(model, prompt, temperature, top_p, n, stream, stop, max_tokens, presence_penalty, frequency_penalty,
                 logit_bias, user):
    print("Sending request to OpenAI API...", "model = ", model, "\ntemperature = ", temperature, "\ntop_p = ", top_p,
          "\nn = ", n, "\nstream = ", stream, "\nstop = ", stop, "\nmax_tokens = ", max_tokens, "\npresence_penalty = ",
          presence_penalty, "\nfrequency_penalty = ", frequency_penalty, "\nlogit_bias = ", logit_bias,
          "\nuser = ", user)
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        logit_bias=logit_bias,
        user=user
    )
    return response


def is_valid_api_key(api_key):
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


def get_model_names(api_key):
    # if __name__ == "__main__":
    #     api_key = os.environ.get("OPENAI_API_KEY")
    #     print("API Key:  ", api_key)
    #     model_names = get_model_names(api_key)
    #     print(model_names)
    url = "https://api.openai.com/v1/models"
    authorization_string = f"Bearer {api_key}"
    headers = {
        "Authorization": authorization_string
    }

    # List to store model names
    model_names = []

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        models = response.json()
        for model in models['data']:
            model_name = model.get('id', 'N/A')
            model_names.append(model_name)
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return model_names


def populate_model_list(context_window, api_key):
    """Iterates through the set of models in the context_window global variable and tries an api call for that model
       using the is_valid_api_key_model function. If the API call is successful, adds the model name to the model_list,
       otherwise proceeds to the next model in the context_window list. When all models have been tested, returns the
       model_list.

  Args:
    api_key: The OpenAI API key to use for the API calls.
    context_window: A dictionary of model names and context window sizes.

  Returns:
    A list of the model names that are valid for the provided API key.
  """

    model_list = []
    for model_name, context_window in context_window.items():
        print(f"Testing {model_name}...")
        if not is_valid_api_key_model(api_key, model_name):
            model_list.append(model_name)

    return model_list


# Checks to see which ChatCompletion Models the API key has access to
def is_valid_api_key_model(api_key, test_model):
    openai.api_key = api_key
    error_messages = []
    print("Validating API key by calling OpenAI API")
    try:
        response = openai.ChatCompletion.create(
            model=test_model,
            messages=[{"role": "user", "content": "Hello, world!"}],
            temperature=0.9, top_p=1, n=1, stream=False, max_tokens=5,
            presence_penalty=0, frequency_penalty=0, logit_bias={}, user=""
        )
        print("This API key/model combination is valid. Model Response:")
        print(response['choices'][0]['message']['content'])
    except openai.OpenAIError as e:
        print(f"Error: {e}")
        error_messages.append(str(e))
    return error_messages


# TODO: The error message in this function is not relevant to this application. Need to change it.
def notify_invalid_key(errors, api_key):
    print("OpenAI API call failed. Notifying user that API Key is invalid")
    error_message = "\n".join(errors)
    message = f"Invalid API Key: {api_key}\n{error_message}"
    messagebox.showerror("Invalid API Key", message)


def get_api_key(parent):
    while True:
        api_key = prompt_for_api_key(parent)
        test_model = "gpt-3.5-turbo"

        # Validate the API key
        print("User entered API Key. Validating...")
        errors = is_valid_api_key_model(api_key, test_model)

        if errors:
            # Notify the user in the Tkinter dialogue and allow them to correct the API Key
            print("API Key is invalid. Prompting user to correct API Key")
            notify_invalid_key(errors, api_key)
            continue  # Skip the rest of the loop and return to the start
        else:
            # Return API Key
            print("API Key is valid. Returning it: ", api_key)
            return api_key  # End the loop and return the API key


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.entry = None
        self.result = None
        super().__init__(parent, title=title)

    def body(self, parent):
        tk.Label(parent, text="Enter your OpenAI API Key:").grid(row=0)
        self.entry = tk.Entry(parent, width=75)
        self.entry.grid(row=1, padx=10, pady=10)
        return self.entry

    def apply(self):
        self.result = self.entry.get()


def prompt_for_api_key(parent):
    print("Opening dialog to prompt user for API Key")
    dialog = CustomDialog(parent, "OpenAI API Key")
    api_key = dialog.result
    return api_key
