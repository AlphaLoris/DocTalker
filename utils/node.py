"""
node.py Module

This module provides utility functions and classes for working with document nodes and sentences. It includes functions
for generating unique IDs, counting tokens, reading/writing document nodes from/to files, and classes for DocumentNode
and Sentence.

Functions:
    - generate_unique_id: Generates a unique ID using UUID.
    - num_tokens_from_messages: Returns the number of tokens used by a list of messages.
    - write_document_nodes_to_file: Writes document nodes to a file in JSON format.
    - read_document_nodes_from_file: Reads document nodes from a file in JSON format.

Classes:
    - DocumentNode: Represents a document node with title, headings, body text, page numbers, and related properties.
    - Sentence: Represents a sentence within a document node with text, ID, and related properties.
    - NodeFactory: Factory class for creating document nodes.
    - SentenceFactory: Factory class for creating sentences.

Notes:
    - The DocumentNode and Sentence classes provide methods for string representation and conversion to/from
        dictionaries.
    - The write_document_nodes_to_file and read_document_nodes_from_file functions facilitate saving/loading document
        nodes.
    - The generate_unique_id function generates a unique ID using UUID.
    - The num_tokens_from_messages function counts the number of tokens used by a list of messages.
"""

from uuid import UUID
import uuid
import re
from typing import List, Optional
import numpy as np
import json
from utils.log_config import setup_colored_logging
import logging
from utils.open_ai_capabilities import num_tokens_from_messages

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)


def generate_unique_id() -> str:
    """
    Generates a unique ID using UUID. Used for document nodes and sentences.

    :return: A unique ID
    :rtype: str
    """
    unique_id = str(uuid.uuid4())
    logger.debug("Generated unique ID: %s", unique_id)
    return unique_id


def write_document_nodes_to_file(document_nodes_dict: dict, output_file_path: str) -> None:
    logger.debug("Writing document nodes to file in write_document_nodes_to_file. Path: %s", output_file_path)
    """
    Writes document nodes to a file in JSON format.

    :param document_nodes_dict: Dictionary of document nodes to write to file
    :type document_nodes_dict: dict
    :param output_file_path: Path of the output file
    :type output_file_path: str
    """
    with open(output_file_path, 'w') as output_file:
        json.dump(
            {k: v.to_dict() for k, v in document_nodes_dict.items()},
            output_file,
            ensure_ascii=False,
            indent=4
        )
    logger.debug("Document nodes written to file in write_document_nodes_to_file. Path: %s", output_file_path)


def read_document_nodes_from_file(input_file_path: str) -> dict:
    logger.debug("Reading document nodes from file in read_document_nodes_from_file. Path: %s", input_file_path)
    """
    Reads document nodes from a file in JSON format.

    :param input_file_path: Path of the input file
    :type input_file_path: str
    :return: Dictionary of document nodes read from file
    :rtype: dict
    """
    document_nodes_dict = {}

    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)

    for node_id, node_dict in data.items():
        node = DocumentNode.from_dict(node_dict)
        document_nodes_dict[node_id] = node

    logger.debug("Document nodes read from file in read_document_nodes_from_file. Path: %s", input_file_path)
    return document_nodes_dict


class DocumentNode:
    def __init__(self, title: str, headings: str, body_text: str, page_numbers: Optional[List[int]],
                 prev_node: Optional[str] = None, next_node: Optional[str] = None) -> None:
        """
        Represents a document node with title, headings, body text, page numbers, the ids of the previous and next nodes
        to maintain the relative order of the document text, a list of the individual sentences within the body text, a
        count of the number of tokens the text represents as the basis for sizing it when composing a prompt for a model
        with a limited context window; the embedding of the text, the name of the model used to generate the embedding,
        and the number of tokens consumed when generating the embedding.

        :param title: Title of the document node
        :type title: str
        :param headings: Headings in the document node
        :type headings: str
        :param body_text: Body text of the document node
        :type body_text: str
        :param page_numbers: List of page numbers associated with the document node
        :type page_numbers: Optional[List[int]]
        :param prev_node: ID of the previous node
        :type prev_node: Optional[str]
        :param next_node: ID of the next node
        :type next_node: Optional[str]
        """
        logger.debug("Creating document node in DocumentNode.__init__")
        self.id = generate_unique_id()
        self.title = title
        self.headings = headings
        self.body_text = body_text
        self.page_numbers = page_numbers
        self.prev_node = prev_node
        self.next_node = next_node
        self.sentence_list = self.create_sentence_list()
        # TODO: Need to pass in the model when this is called, and need to pass the model when this is called:
        self.tokens_count = num_tokens_from_messages([self.headings, self.body_text]) - 10
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0

    def create_sentence_list(self) -> List['Sentence']:
        logger.debug("Creating the sentence list in DocumentNode.create_sentence_list")
        """
        Splits the document's body text into individual sentences and returns them as Sentence objects. The sentences
        will be used to incrementally expand the node text when composing a prompt for a model with a limited context
        window.

        :return: A list of Sentence objects
        :rtype: List['Sentence']
        """
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', self.body_text)
        sentence_objects = []
        for i, sentence_text in enumerate(sentences):
            # Check if the sentence_text is not empty after stripping whitespace characters
            if sentence_text.strip():
                prev_sentence = sentence_objects[-1].id if i > 0 else None
                sentence = SentenceFactory.create_sentence(sentence_text=sentence_text, prev_sentence=prev_sentence)
                logger.info("Sentence text being added to the sentence object:", sentence_text)
                sentence_objects.append(sentence)
                if i > 0:
                    sentence_objects[i - 1].next_sentence = sentence.id
            else:
                logger.info(f"Empty sentence detected after splitting at index {i}. Original sentence text: '"
                            f"{sentence_text}'")
        logger.info(f"Total sentences detected: {len(sentence_objects)}")
        logger.debug("Sentence list created in DocumentNode.create_sentence_list")
        return sentence_objects

    def to_string(self) -> str:
        logger.debug(f"Converting document node {self.id} to string in DocumentNode.to_string")
        """
        Returns a string representation of the DocumentNode object.

        :return: A string representation of the DocumentNode object
        :rtype: str
        """
        result = ""
        result += "prev_node:\n" + str(self.prev_node) + "\n\n"
        result += "id:\n" + str(self.id) + "\n\n"
        result += "title:\n" + self.title + "\n\n"
        result += "headings:\n" + self.headings + "\n\n"
        result += "body_text:\n" + self.body_text + "\n\n"
        if self.page_numbers is not None:
            result += "page_numbers:\n" + ', '.join(map(str, self.page_numbers)) + "\n\n"
        else:
            result += "page_numbers: None\n\n"
        result += "tokens_count:\n" + str(self.tokens_count) + "\n\n"
        result += "embedding_model:\n" + self.embedding_model + "\n\n"
        result += "token_usage\n" + str(self.token_usage) + "\n\n"
        result += "sentence_list:\n" + "\n".join([sentence.to_string() for sentence in self.sentence_list]) + "\n\n"
        result += "embedding:\n" + str(self.embedding) + "\n\n"
        result += "next_node:\n" + str(self.next_node) + "\n\n"
        result += "\n"
        logger.debug(f"Document node {self.id} converted to string in DocumentNode.to_string")
        return result

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the DocumentNode object when it is serialized to JSON.

        :return: A dictionary representation of the DocumentNode object
        :rtype: dict
        """
        logger.debug(f"Converting document node {self.id} to dictionary in DocumentNode.to_dict")
        return {
            "prev_node": self.prev_node,
            "id": str(self.id),
            "title": self.title,
            "headings": self.headings,
            "body_text": self.body_text,
            "page_numbers": self.page_numbers if self.page_numbers is not None else None,
            "tokens_count": self.tokens_count,
            "embedding_model": self.embedding_model,
            "token_usage": self.token_usage,
            "sentence_list": [sentence.to_dict() for sentence in self.sentence_list],
            "embedding": self.embedding.tolist() if self.embedding is not None else None,
            "next_node": self.next_node,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentNode':
        """
        Creates a DocumentNode object from a dictionary representation when it is deserialized from JSON.

        :param data: A dictionary representation of a DocumentNode object
        :type data: dict
        :return: A DocumentNode object
        :rtype: DocumentNode
        """
        logger.debug(f"Creating document node from dictionary in DocumentNode.from_dict")
        node = cls(
            title=data["title"],
            headings=data["headings"],
            body_text=data["body_text"],
            page_numbers=data["page_numbers"],
            prev_node=data["prev_node"],
            next_node=data["next_node"],
        )
        node.id = uuid.UUID(data["id"])
        node.tokens_count = data["tokens_count"]
        node.embedding_model = data["embedding_model"]
        node.token_usage = data["token_usage"]
        node.embedding = np.array(data["embedding"]) if data["embedding"] is not None else None
        node.sentence_list = [Sentence.from_dict(sentence_data) for sentence_data in data["sentence_list"]]
        return node


class Sentence:
    def __init__(self, sentence_id: uuid, sentence_text: str, prev_sentence: Optional[UUID] = None,
                 next_sentence: Optional[UUID] = None) -> None:
        # TODO: It may make sense to add a reference to the document node that the sentence belongs to.
        # TODO: Do the first and last sentences within this node have links to the sentences in the previous and next
        #  nodes?
        """
        Represents a sentence within a document node with text, ID, links to the previous and next sentences in the
        document node.

        :param sentence_id: ID of the sentence
        :type sentence_id: str
        :param sentence_text: Text of the sentence
        :type sentence_text: str
        :param prev_sentence: ID of the previous sentence
        :type prev_sentence: Optional[str]
        :param next_sentence: ID of the next sentence
        :type next_sentence: Optional[str]
        """
        self.id = sentence_id
        self.text = sentence_text
        self.prev_sentence = prev_sentence
        self.next_sentence = next_sentence
        self.tokens_count = num_tokens_from_messages([self.text]) - 6
        self.embedding = np.zeros((1, 1536))
        self.embedding_model = ""
        self.token_usage = 0
        logger.debug("Sentence created in Sentence.__init__")

    def to_string(self) -> str:
        """
        Returns a string representation of the Sentence object.

        :return: A string representation of the Sentence object
        :rtype: str
        """
        logger.debug(f"Converting sentence {self.id} to string in Sentence.to_string")
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

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the Sentence object as part of serializing the sentence to a file.

        :return: A dictionary representation of the Sentence object
        :rtype: dict
        """
        logger.debug(f"Converting sentence {self.id} to dictionary in Sentence.to_dict")
        return {
            "prev_sentence": self.prev_sentence,
            "id": str(self.id),
            "text": self.text,
            "tokens_count": self.tokens_count,
            "embedding_model": self.embedding_model,
            "token_usage": self.token_usage,
            "embedding": self.embedding.tolist() if self.embedding is not None else None,
            "next_sentence": self.next_sentence,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Sentence':
        """
        Creates a Sentence object from a dictionary representation as part of deserializing the sentence from a file.

        :param data: A dictionary representation of a Sentence object
        :type data: dict
        :return: A Sentence object
        :rtype: Sentence
        """
        logger.debug(f"Creating sentence from dictionary in Sentence.from_dict")
        sentence = cls(
            sentence_id=uuid.UUID(data["id"]),
            sentence_text=data["text"],
            prev_sentence=data["prev_sentence"],
            next_sentence=data["next_sentence"],
        )
        sentence.tokens_count = data["tokens_count"]
        sentence.embedding_model = data["embedding_model"]
        sentence.token_usage = data["token_usage"]
        sentence.embedding = np.array(data["embedding"]) if data["embedding"] is not None else None
        return sentence


class NodeFactory:
    @classmethod
    def create_node(cls, title: str, headings: str, body_text: str, prev_node: Optional[UUID] = None,
                    next_node: Optional[UUID] = None) -> DocumentNode:
        logger.debug("Creating document node in NodeFactory.create_node")
        """
        Factory method to create a DocumentNode object.

        :param title: Title of the document node
        :type title: str
        :param headings: Headings in the document node
        :type headings: str
        :param body_text: Body text of the document node
        :type body_text: str
        :param prev_node: ID of the previous node
        :type prev_node: Optional[str]
        :param next_node: ID of the next node
        :type next_node: Optional[str]
        :return: A DocumentNode object
        :rtype: DocumentNode
        """
        return DocumentNode(title, headings, body_text, prev_node, next_node)


class SentenceFactory:
    @classmethod
    def create_sentence(cls, sentence_text: str, prev_sentence: Optional[str] = None,
                        next_sentence: Optional[str] = None) -> Sentence:
        logger.debug("Creating sentence in SentenceFactory.create_sentence")
        """
        Factory method to create a Sentence object.

        :param sentence_text: Text of the sentence
        :type sentence_text: str
        :param prev_sentence: ID of the previous sentence
        :type prev_sentence: Optional[str]
        :param next_sentence: ID of the next sentence
        :type next_sentence: Optional[str]
        :return: A Sentence object
        :rtype: Sentence
        """
        sentence_id = generate_unique_id()
        return Sentence(sentence_id, sentence_text, prev_sentence, next_sentence)
