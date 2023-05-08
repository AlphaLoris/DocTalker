# TODO: Develop ways to understand the embeddings
# TODO: Remove the OpenAI API key from the code
import os
import re
import numpy as np
from src.node import generate_unique_id, num_tokens_from_messages
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

if openai.api_key:
    # Use the API key in your script
    print("API key found.")
else:
    print("API key not found.")


class KeyWord:
    def __init__(self, keyword_id, keyword):
        self.id = keyword_id
        self.word = keyword
        self.tokens_count = num_tokens_from_messages([self.word]) - 6
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0

    def to_string(self):
        result = ""
        result += "id:\n" + str(self.id) + "\n\n"
        result += "tokens_count:\n" + str(self.tokens_count) + "\n\n"
        result += "word:\n" + self.word + "\n\n"
        result += "embedding_model:\n" + str(self.embedding_model) + "\n\n"
        result += "token_usage:\n" + str(self.token_usage) + "\n\n"
        result += "embedding:\n" + str(self.embedding) + "\n\n"
        result += "\n"
        return result


def create_keyword_objects_from_txt(keyword_file_path: str) -> dict:
    keywords_dict = {}

    with open(keyword_file_path, 'r') as file:
        text = file.read()
        words = re.findall(r'\w+', text)

    for word in words:
        keyword_id = generate_unique_id()
        keyword_obj = KeyWord(keyword_id, word)
        keywords_dict[keyword_id] = keyword_obj

    return keywords_dict


def write_keywords_objects_to_file(keywords_dict: dict, output_file_path: str):
    with open(output_file_path, 'w') as output_file:
        for keyword_obj in keywords_dict.values():
            output_file.write(keyword_obj.to_string())
            output_file.write("-----\n")


def read_keyword_objects_from_file(input_file_path: str) -> dict:
    keywords_dict = {}

    with open(input_file_path, 'r') as input_file:
        keyword_lines = input_file.readlines()

    keyword_id = None
    keyword = None
    tokens_count = None
    embedding_model = None
    token_usage = None
    embedding = []

    for line in keyword_lines:
        if line.startswith("id:"):
            keyword_id = line.strip().split(":")[1].strip()
        elif line.startswith("tokens_count:"):
            tokens_count = int(line.strip().split(":")[1].strip())
        elif line.startswith("text:"):
            keyword = line.strip().split(":")[1].strip()
        elif line.startswith("embedding_model:"):
            embedding_model = line.strip().split(":")[1].strip()
        elif line.startswith("token_usage:"):
            token_usage = int(line.strip().split(":")[1].strip())
        elif line.startswith("embedding:"):
            embedding = np.array(eval(line.strip().split(":")[1].strip()))
        elif line.startswith("-----"):
            if keyword_id and keyword and tokens_count is not None:
                keyword_obj = KeyWord(keyword_id, keyword)
                keyword_obj.tokens_count = tokens_count
                keyword_obj.embedding_model = embedding_model
                keyword_obj.token_usage = token_usage
                keyword_obj.embedding = embedding
                keywords_dict[keyword_id] = keyword_obj
                keyword_id = None
                keyword = None
                tokens_count = None
                embedding_model = None
                token_usage = None
                embedding = []

    return keywords_dict


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, model="text-embedding-ada-002") -> dict:
    return openai.Embedding.create(input=[text], model=model)


def generate_embedding(obj) -> None:
    # Determine the appropriate text attribute for the object
    if hasattr(obj, "body_text"):
        # Object is a Node
        text = obj.headings + ": " + obj.body_text
    elif hasattr(obj, "text"):
        # Object is a Sentence
        text = obj.text
    elif hasattr(obj, "word"):
        # Object is a Keyword
        text = obj.word
    else:
        print("Object causing error: ", obj.id)
        raise ValueError(f"Unsupported object type: {type(obj).__name__}")

    # Check if the text is empty or contains only whitespace
    if text.strip() == "":
        return

    # Generate the embedding and get the response
    print("Generating embedding for: ", obj.id)
    print("Text: ", text)
    response = get_embedding(text)
    print("Response received for: ", obj.id)

    # Extract values from the response JSON
    embedding = response["data"][0]["embedding"]
    model = response["model"]
    total_tokens = response["usage"]["total_tokens"]

    # Assign the values to the relevant attributes
    obj.embedding = np.array(embedding).reshape(1, -1)
    obj.embedding_model = model
    obj.token_usage = total_tokens
