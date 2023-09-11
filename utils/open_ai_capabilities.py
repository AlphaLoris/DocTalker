import tkinter as tk
from tkinter import simpledialog, messagebox
import tiktoken
import openai
import requests
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)


# Function to determine the number of tokens in a message
def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    logger.debug(f"Counting the number of tokens in the prompt messages in num_tokens_from_messages()"
                 f" called with {len(messages)} messages and model {model}")
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.error("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        logger.info("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        logger.info("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}.
             See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are 
             converted to tokens."""
        )
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
    logger.debug("Sending request to OpenAI API in send_request()")
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
    logger.debug("Response received from OpenAI API in send_request()")
    return response


def is_valid_api_key(api_key):
    logger.debug("Validating API key in is_valid_api_key()")
    openai.api_key = api_key
    error_messages = []
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, world!"}],
            temperature=0.9, top_p=1, n=1, stream=False, max_tokens=5, presence_penalty=0, frequency_penalty=0,
            logit_bias={}, user=""
        )
        logger.info(f"API Key is valid. Model Response:", response['choices'][0]['message']['content'])
    except openai.OpenAIError as e:
        logger.error(f"Error: {e}")
        error_messages.append(str(e))
    return error_messages


def get_model_names(api_key):
    logger.debug("Getting model names in get_model_names()")
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
        logger.error(f"Error: {response.status_code}, {response.text}")

    logger.debug("Returning model names in get_model_names()")
    return model_names


def populate_model_list(context_window, api_key):
    logger.debug("Populating model list in populate_model_list()")
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

    logger.debug("Returning model list in populate_model_list()")
    return model_list


# Checks to see which ChatCompletion Models the API key has access to
def is_valid_api_key_model(api_key, test_model):
    logger.debug("Validating API key in is_valid_api_key_model()")
    openai.api_key = api_key
    logger.info("API key to be validated in is_valid_api_key_model: ", openai.api_key)
    error_messages = []
    logger.debug("Validating API key by calling OpenAI API")
    try:
        response = openai.ChatCompletion.create(
            model=test_model,
            messages=[{"role": "user", "content": "Hello, world!"}],
            temperature=0.9, top_p=1, n=1, stream=False, max_tokens=5,
            presence_penalty=0, frequency_penalty=0, logit_bias={}, user=""
        )
        logger.info(f"This API key/model combination is valid. Model Response:",
                    response['choices'][0]['message']['content'])
    except openai.OpenAIError as e:
        logger.error(f"Error: {e}")
        error_messages.append(str(e))
    return error_messages


# TODO: The error message in this function is not relevant to this application. Need to change it.
def notify_invalid_key(errors, api_key):
    logger.debug("OpenAI API call failed. Notifying user that API Key is invalid")
    error_message = "\n".join(errors)
    message = f"Invalid API Key: {api_key}\n{error_message}"
    messagebox.showerror("Invalid API Key", message)


def get_api_key(parent):
    logger.debug("Getting API key in get_api_key()")
    while True:
        logger.info("Prompting user for API Key in get_api_key")
        api_key = prompt_for_api_key(parent)
        test_model = "gpt-3.5-turbo"

        # Validate the API key
        logger.info(f"User entered API Key. Validating...", "API Key: ", api_key)
        # Check if the user cancelled the dialog or entered an empty string
        if not api_key:
            logger.info("User cancelled or entered an empty API key.")
            return None

        errors = is_valid_api_key_model(api_key, test_model)

        if errors:
            # Notify the user in the Tkinter dialogue and allow them to correct the API Key
            logger.error("API Key is invalid. Prompting user to correct API Key")
            notify_invalid_key(errors, api_key)
            continue  # Skip the rest of the loop and return to the start
        else:
            # Return API Key
            logger.info("API Key is valid. Returning it: ", api_key)
            return api_key  # End the loop and return the API key


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.entry = None
        self.result = None
        super().__init__(parent, title=title)
        logger.debug("Initializing CustomDialog")

    def body(self, parent):
        tk.Label(parent, text="Enter your OpenAI API Key:").grid(row=0)
        self.entry = tk.Entry(parent, width=75)
        self.entry.grid(row=1, padx=10, pady=10)
        return self.entry

    def apply(self):
        self.result = self.entry.get()


def prompt_for_api_key(parent):
    logger.debug("Prompting user for API Key in prompt_for_api_key()")
    logger.info("Opening dialog to prompt user for API Key")
    dialog = CustomDialog(parent, "OpenAI API Key")
    api_key = dialog.result
    logger.debug("Returning API Key in prompt_for_api_key()")
    return api_key
