"""
embeddings.py Module

This module provides functions and classes for working with embeddings, including generating and storing embeddings for
keywords and text.

Functions:
    - create_keyword_objects_from_txt: Create keyword objects from a text file.
    - write_keywords_objects_to_file: Write keyword objects to a file in JSON format.
    - read_keyword_objects_from_file: Read keyword objects from a file in JSON format.
    - get_embedding: Retrieve the embedding for a given text using the OpenAI API.
    - generate_embedding: Generate and assign embeddings for keyword, node, or sentence objects.

Classes:
    - KeyWord: Represents a keyword with an ID, word, and related properties.

Notes:
    - This module assumes that the required dependencies are installed and properly imported.
    - The create_keyword_objects_from_txt function reads keywords from a text file and creates KeyWord objects.
    - The write_keywords_objects_to_file and read_keyword_objects_from_file functions facilitate saving/loading keyword
        objects.
    - The KeyWord class provides methods for string representation and conversion to/from dictionaries.
    - The get_embedding function retrieves the embedding for a given text using the OpenAI API.
    - The generate_embedding function generates and assigns embeddings for keyword, node, or sentence objects.
"""

import os
import re
import json
import numpy as np
from src.node import generate_unique_id, num_tokens_from_messages
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
from typing import List, Dict, Union
from node import DocumentNode, Sentence


# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

if openai.api_key:
    # Use the API key in your script
    print("API key found.")
else:
    print("API key not found.")


class KeyWord:
    """
    Class that represents a keyword with an ID, word, and related properties.
    """
    def __init__(self, keyword_id: str, keyword: str):
        """
        Constructor for the KeyWord class.

        :param keyword_id: ID of the keyword
        :type keyword_id: str
        :param keyword: The keyword itself
        :type keyword: str
        """
        self.id = keyword_id
        self.word = keyword
        self.tokens_count = num_tokens_from_messages([self.word]) - 6
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0

    def to_string(self) -> str:
        """
        Converts the keyword object to a string.

        :return: String representation of the keyword object
        :rtype: str
        """
        result = ""
        result += "id:\n" + str(self.id) + "\n\n"
        result += "tokens_count:\n" + str(self.tokens_count) + "\n\n"
        result += "word:\n" + self.word + "\n\n"
        result += "embedding_model:\n" + str(self.embedding_model) + "\n\n"
        result += "token_usage:\n" + str(self.token_usage) + "\n\n"
        result += "embedding:\n" + str(self.embedding) + "\n\n"
        result += "\n"
        return result

    def to_dict(self) -> Dict[str, Union[int, str, List[float]]]:
        """
        Converts the keyword object to a dictionary.

        :return: Dictionary representation of the keyword object
        :rtype: dict
        """
        return {
            "id": self.id,
            "word": self.word,
            "tokens_count": self.tokens_count,
            "embedding": self.embedding.tolist(),  # np.ndarray to list
            "embedding_model": self.embedding_model,
            "token_usage": self.token_usage
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[int, str, List[float]]]) -> 'KeyWord':
        """
        Creates a keyword object from a dictionary.

        :param data: Dictionary representing a keyword object
        :type data: dict
        :return: Keyword object created from the dictionary
        :rtype: KeyWord
        """
        keyword = cls(data["id"], data["word"])
        keyword.tokens_count = data["tokens_count"]
        keyword.embedding = np.array(data["embedding"])  # list to np.ndarray
        keyword.embedding_model = data["embedding_model"]
        keyword.token_usage = data["token_usage"]
        return keyword


def create_keyword_objects_from_txt(keyword_file_path: str) -> Dict[str, KeyWord]:
    """
    Creates keyword objects from a text file.

    :param keyword_file_path: Path to the text file
    :type keyword_file_path: str
    :return: Dictionary of keyword objects
    :rtype: dict
    """
    keywords_dict = {}

    with open(keyword_file_path, 'r') as file:
        text = file.read()
        words = re.findall(r'\w+', text)

    for word in words:
        keyword_id = generate_unique_id()
        keyword_obj = KeyWord(keyword_id, word)
        keywords_dict[keyword_id] = keyword_obj

    return keywords_dict


def write_keywords_objects_to_file(keywords_dict: Dict[str, KeyWord], output_file_path: str) -> None:
    """
    Writes keyword objects to a file in JSON format.

    :param keywords_dict: Dictionary of keyword objects
    :type keywords_dict: dict
    :param output_file_path: Path to the output file
    :type output_file_path: str
    """
    with open(output_file_path, 'w') as output_file:
        json.dump(
            {k: v.to_dict() for k, v in keywords_dict.items()},
            output_file,
            ensure_ascii=False,
            indent=4
        )


def read_keyword_objects_from_file(input_file_path: str) -> Dict[str, KeyWord]:
    """
    Reads keyword objects from a file in JSON format.

    :param input_file_path: Path to the input file
    :type input_file_path: str
    :return: Dictionary of keyword objects
    :rtype: dict
    """
    keywords_dict = {}

    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)

    for keyword_id, keyword_dict in data.items():
        keyword = KeyWord.from_dict(keyword_dict)
        keywords_dict[keyword_id] = keyword

    return keywords_dict


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, model="text-embedding-ada-002") -> Dict[str, Union[str, List[float]]]:
    """
    Retrieves the embedding for a given text using the OpenAI API.

    :param text: Text to retrieve the embedding for
    :type text: str
    :param model: Model to use for the embedding
    :type model: str
    :return: Embedding for the text
    :rtype: dict
    """
    return openai.Embedding.create(input=[text], model=model)


def generate_embedding(obj: Union[KeyWord, DocumentNode, Sentence]) -> None:
    """
    Generates and assigns embeddings for keyword, node, or sentence objects.

    :param obj: Object to generate an embedding for
    :type obj: Union[KeyWord, Node, Sentence]
    """
    # Determine the appropriate text attribute for the object
    if hasattr(obj, "body_text"):
        # Object is a Node
        text = obj.headings + ": " + obj.body_text
        print("Embedding node text: ", obj.body_text)
    elif hasattr(obj, "text"):
        # Object is a Sentence
        text = obj.text
        print("Embedding sentence text: ", obj.text)
    elif hasattr(obj, "word"):
        # Object is a Keyword
        print("Embedding keyword text: ", obj.word)
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
    try:
        embedding = response["data"][0]["embedding"]
        model = response["model"]
        total_tokens = response["usage"]["total_tokens"]
    except KeyError as e:
        raise RuntimeError(f"Failed to parse response: missing key {e}")

    # Assign the values to the relevant attributes
    print("Assigning embedding value to: ", obj.id)
    obj.embedding = np.array(embedding).reshape(1, -1)
    obj.embedding_model = model
    obj.token_usage = total_tokens
    print("Embedding value assigned to: ", obj.id)
