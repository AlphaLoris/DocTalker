# document_manager.py module

"""
document_manager.py

This module provides a DocumentManager class for managing documents, keywords, embeddings, and Faiss indexing. The
DocumentManager class handles document parsing, keyword extraction, embedding generation, Faiss index building, and
saving/loading of manager state.

Usage:
    1. Create an instance of the DocumentManager class.
    2. Use the provided methods to load documents, keywords, build the Faiss index, search for similar nodes, and
     save/load the manager state.

Dependencies:
    - List, Tuple from typing
    - DocxDocumentParser from src.docx_document_parser
    - create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file,
      read_keyword_objects_from_file from embeddings
    - FaissIndex from faiss_index
    - np from numpy

Notes:
    - The DocumentManager class tracks document nodes, keyword objects, Faiss index, embedding order, and statistics.
    - The load_documents method parses and processes document files, generating embeddings for nodes and sentences.
    - The load_keywords method creates keyword objects, generates embeddings, and updates the embedding order.
    - The build_faiss_index method builds the Faiss index using document and keyword embeddings.
    - The search_similar_nodes method performs a search using a query embedding and returns similar nodes.
    - The save_manager_state method saves document nodes, keyword objects, and the Faiss index to files.
    - The load_manager_state method loads document nodes, keyword objects, and the Faiss index from files.
"""

from typing import List, Tuple
from src.docx_document_parser import DocxDocumentParser
from embeddings import create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file, \
    read_keyword_objects_from_file
from faiss_index import FaissIndex
from node import write_document_nodes_to_file, read_document_nodes_from_file
import numpy as np


class DocumentManager:
    def __init__(self):
        self.document_nodes = {}
        self.keyword_objects = {}
        self.faiss_index = None
        self.embedding_order = []
        self.total_sentences = 0
        self.total_document_nodes = 0
        self.total_keywords = 0

    """
    def load_documents(self, file_paths: List[str]):
        print("load_documents called")
        for file_path in file_paths:
            print("Parsing document: " + file_path)
            parser = DocxDocumentParser(file_path)
            print("Document parsed: " + file_path)
            nodes = parser.process_document()
            print("Returned from process_document() with nodes")
            for node_id, node in nodes.items():
                print("Generating node embedding for: " + node.body_text)
                generate_embedding(node)
                print("Node embedding generated.")
                self.total_document_nodes += 1
                self.embedding_order.append(('node', node_id))
                for sentence in node.create_sentence_list():
                    print("Generating sentence embedding for: " + sentence.text)
                    generate_embedding(sentence)
                    print("Sentence embedding generated.")
                    self.embedding_order.append(('sentence', sentence.id))
                    self.total_sentences += 1
            self.document_nodes.update(nodes)
        print("load_documents complete.")
        print(f"Total document nodes: {self.total_document_nodes}")
        print(f"Total sentences: {self.total_sentences}")
    """

    def load_documents(self, file_paths: List[str]):
        print("load_documents called")
        for file_path in file_paths:
            print("Parsing document: " + file_path)
            parser = DocxDocumentParser(file_path)
            print("Document parsed: " + file_path)
            nodes = parser.process_document()
            print("Returned from process_document() with nodes")
            for node_id, node in nodes.items():
                print("Generating node embedding for: " + node.body_text)
                generate_embedding(node)
                print("Node embedding generated.")
                self.total_document_nodes += 1
                self.embedding_order.append(('node', node_id))
                for sentence in node.sentence_list:  # Access the sentence_list attribute directly
                    print("Generating sentence embedding for: " + sentence.text)
                    generate_embedding(sentence)
                    print("Sentence embedding generated.")
                    self.embedding_order.append(('sentence', sentence.id))
                    self.total_sentences += 1
            self.document_nodes.update(nodes)
        print("load_documents complete.")
        print(f"Total document nodes: {self.total_document_nodes}")
        print(f"Total sentences: {self.total_sentences}")

    def load_keywords(self, keyword_file_path: str):
        print("load_keywords called")
        self.keyword_objects = create_keyword_objects_from_txt(keyword_file_path)
        for keyword in self.keyword_objects.values():
            print("Generating keyword embedding for: " + keyword.word)
            generate_embedding(keyword)
            print("Keyword embedding generated.")
            self.embedding_order.append(('keyword', keyword.id))
            self.total_keywords += 1
        print("load_keywords completed")
        print(f"Total keywords: {self.total_keywords}")

    """
    def build_faiss_index(self):
        embeddings = []
        print("Length of embedding_order before building the index:", len(self.embedding_order))
        for node in self.document_nodes.values():
            embeddings.append(node.embedding)
            for sentence in node.create_sentence_list():
                embeddings.append(sentence.embedding)
        for keyword in self.keyword_objects.values():
            embeddings.append(keyword.embedding)

        self.faiss_index = FaissIndex(embeddings)
        self.faiss_index.create_index()
    """

    def build_faiss_index(self):
        embeddings = []
        print("Length of embedding_order before building the index:", len(self.embedding_order))
        for node in self.document_nodes.values():
            embeddings.append(node.embedding)
            for sentence in node.sentence_list:  # Use the stored sentence list
                embeddings.append(sentence.embedding)
        for keyword in self.keyword_objects.values():
            embeddings.append(keyword.embedding)

        self.faiss_index = FaissIndex(embeddings)
        self.faiss_index.create_index()

    def search_similar_nodes(self, query_embedding: List[float], k: int) -> Tuple[List[int], List[float]]:
        indices, distances = self.faiss_index.search(np.array([query_embedding]), k)
        return indices[0].tolist(), distances[0].tolist()

    def save_manager_state(self, output_directory: str):
        write_document_nodes_to_file(self.document_nodes, f"{output_directory}/document_nodes.txt")
        write_keywords_objects_to_file(self.keyword_objects, f"{output_directory}/keywords.txt")
        self.faiss_index.save_index(f"{output_directory}/faiss_index")

    def load_manager_state(self, input_directory: str):
        self.document_nodes = read_document_nodes_from_file(f"{input_directory}/document_nodes.txt")
        self.keyword_objects = read_keyword_objects_from_file(f"{input_directory}/keywords.txt")

        # Clear the embedding order list
        self.embedding_order = []

        # Rebuild the embedding order list for nodes
        for node_id in self.document_nodes:
            self.embedding_order.append(('node', node_id))
            for sentence in self.document_nodes[node_id].create_sentence_list():
                self.embedding_order.append(('sentence', sentence.id))

        # Rebuild the embedding order list for keywords
        for keyword_id in self.keyword_objects:
            self.embedding_order.append(('keyword', keyword_id))

        self.faiss_index = FaissIndex([])
        self.faiss_index.load_index(f"{input_directory}/faiss_index")

