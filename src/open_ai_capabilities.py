import tiktoken
import openai

# Not implemented -- revise as necessary

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
