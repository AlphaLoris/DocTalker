# node.py module

import uuid
import re
from typing import List
import tiktoken
import numpy as np


def generate_unique_id():
    return str(uuid.uuid4())


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += len(encoding.encode(message))
        num_tokens += 2  # every reply is primed with <im_start>assistant
        print("num_tokens calculated:", num_tokens)
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")


def write_document_nodes_to_file(document_nodes_dict: dict, output_file_path: str):
    with open(output_file_path, 'w') as output_file:
        for document_node in document_nodes_dict.values():
            output_file.write(document_node.to_string())
            output_file.write("=====\n")


def read_document_nodes_from_file(input_file_path: str) -> dict:
    document_nodes_dict = {}

    with open(input_file_path, 'r') as input_file:
        document_node_lines = input_file.read().split("=====\n")

    for document_node_block in document_node_lines[:-1]:  # Exclude the last empty block
        document_node_info = document_node_block.split("\n\n")
        try:
            document_node_info_dict = {info.split(":\n")[0]: info.split(":\n")[1] for info in document_node_info}
        except IndexError:
            print(f"Error: problem with line: {document_node_info} when reading document nodes from file")
            raise

        document_node_id = document_node_info_dict["id"]
        title = document_node_info_dict["title"]
        headings = document_node_info_dict["headings"]
        body_text = document_node_info_dict["body_text"]
        prev_node = document_node_info_dict["prev_node"]
        next_node = document_node_info_dict["next_node"]
        tokens_count = int(document_node_info_dict["tokens_count"])
        embedding_model = document_node_info_dict["embedding_model"]
        token_usage = int(document_node_info_dict["token_usage"])
        embedding = np.fromstring(document_node_info_dict["embedding"].strip("[]"), sep=' ')

        document_node = DocumentNode(title, headings, body_text)
        document_node.id = document_node_id
        document_node.prev_node = prev_node
        document_node.next_node = next_node
        document_node.tokens_count = tokens_count
        document_node.embedding_model = embedding_model
        document_node.token_usage = token_usage
        document_node.embedding = embedding

        sentence_list = []
        sentence_lines = document_node_info_dict["sentence_list"].split("\n")
        for sentence_block in sentence_lines:
            sentence_info = sentence_block.split("\n\n")
            sentence_info_dict = {info.split(":\n")[0]: info.split(":\n")[1] for info in sentence_info}

            sentence_id = sentence_info_dict["id"]
            text = sentence_info_dict["text"]
            prev_sentence = sentence_info_dict["prev_sentence"]
            next_sentence = sentence_info_dict["next_sentence"]
            tokens_count = int(sentence_info_dict["tokens_count"])
            embedding_model = sentence_info_dict["embedding_model"]
            token_usage = int(sentence_info_dict["token_usage"])
            embedding = np.fromstring(sentence_info_dict["embedding"].strip("[]"), sep=' ')

            sentence = Sentence(sentence_id, text, prev_sentence, next_sentence)
            sentence.tokens_count = tokens_count
            sentence.embedding_model = embedding_model
            sentence.token_usage = token_usage
            sentence.embedding = embedding

            sentence_list.append(sentence)

        document_node.sentence_list = sentence_list
        document_nodes_dict[document_node_id] = document_node

    return document_nodes_dict


class DocumentNode:
    def __init__(self, title, headings, body_text, prev_node=None, next_node=None):
        self.id = generate_unique_id()
        self.title = title
        self.headings = headings
        self.body_text = body_text
        self.prev_node = prev_node
        self.next_node = next_node
        self.sentence_list = self.create_sentence_list()
        self.tokens_count = num_tokens_from_messages([self.headings, self.body_text]) - 10
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0

    def create_sentence_list(self) -> List['Sentence']:
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', self.body_text)
        sentence_objects = []
        for i, sentence_text in enumerate(sentences):
            # Check if the sentence_text is not empty after stripping whitespace characters
            if sentence_text.strip():
                prev_sentence = sentence_objects[-1].id if i > 0 else None
                sentence = SentenceFactory.create_sentence(sentence_text=sentence_text, prev_sentence=prev_sentence)
                sentence_objects.append(sentence)
                if i > 0:
                    sentence_objects[i - 1].next_sentence = sentence.id
        return sentence_objects

    def to_string(self):
        result = ""
        result += "prev_node:\n" + str(self.prev_node) + "\n\n"
        result += "id:\n" + str(self.id) + "\n\n"
        result += "title:\n" + self.title + "\n\n"
        result += "headings:\n" + self.headings + "\n\n"
        result += "body_text:\n" + self.body_text + "\n\n"
        result += "tokens_count:\n" + str(self.tokens_count) + "\n\n"
        result += "embedding_model:\n" + self.embedding_model + "\n\n"
        result += "token_usage\n" + str(self.token_usage) + "\n\n"
        result += "sentence_list:\n" + "\n".join([sentence.to_string() for sentence in self.sentence_list]) + "\n\n"
        result += "embedding:\n" + str(self.embedding) + "\n\n"
        result += "next_node:\n" + str(self.next_node) + "\n\n"
        result += "\n"
        return result


class Sentence:
    def __init__(self, sentence_id, sentence_text, prev_sentence=None, next_sentence=None):
        self.id = sentence_id
        self.text = sentence_text
        self.prev_sentence = prev_sentence
        self.next_sentence = next_sentence
        self.tokens_count = num_tokens_from_messages([self.text]) - 6
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0

    def to_string(self):
        result = ""
        result += "prev_sentence:\n" + str(self.prev_sentence) + "\n\n"
        result += "id:\n" + str(self.id) + "\n\n"
        result += "text:\n" + self.text + "\n\n"
        result += "tokens_count:\n" + str(self.tokens_count) + "\n\n"
        result += "embedding_model:\n" + self.embedding_model + "\n\n"
        result += "token_usage\n" + str(self.token_usage) + "\n\n"
        result += "embedding:\n" + str(self.embedding) + "\n\n"
        result += "next_sentence:\n" + str(self.next_sentence) + "\n\n"
        result += "\n"
        return result


class NodeFactory:
    @classmethod
    def create_node(cls, title, headings, body_text, prev_node=None, next_node=None):
        return DocumentNode(title, headings, body_text, prev_node, next_node)


class SentenceFactory:
    @classmethod
    def create_sentence(cls, sentence_text, prev_sentence=None, next_sentence=None):
        sentence_id = generate_unique_id()
        return Sentence(sentence_id, sentence_text, prev_sentence, next_sentence)
