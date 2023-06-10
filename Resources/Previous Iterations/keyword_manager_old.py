"""
keyword_manager.py module

This module provides a KeywordManager class for managing keywords, embeddings, and Faiss indexing. The
KeywordManager class handles keyword extraction, embedding generation, Faiss index building, and
saving/loading of the manager state.

Usage:
1. Create an instance of the KeywordManager class.
2. Use the provided methods to load keywords, build the Faiss index, search for similar keywords, and
save/load the manager state.

Dependencies:
- List, Tuple from typing
- create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file,
read_keyword_objects_from_file from embeddings
- FaissIndex from faiss_index
- np from numpy

Notes:
- The KeywordManager class tracks keyword objects, Faiss index, embedding order, and statistics.
- The load_keywords method creates keyword objects, generates embeddings, and updates the embedding order.
- The build_faiss_index method builds the Faiss index using keyword embeddings.
- The search_similar_nodes method performs a search using a query embedding and returns similar keywords.
- The save_key_manager_state method saves keyword objects and the Faiss index to files.
- The load_keyword_manager_state method loads keyword objects and the Faiss index from files.
"""

from typing import Dict
from embeddings import KeyWord
from typing import List, Tuple
from embeddings import create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file, \
    read_keyword_objects_from_file
from faiss_index import FaissIndex
import numpy as np


class KeywordManager:
    def __init__(self):
        self.keyword_objects = {}
        self.faiss_index = None
        self.embedding_order = []
        self.total_sentences = 0
        self.total_keywords = 0

    def generate_keyword_embedding(self, keyword):
        print("Generating keyword embedding for: " + keyword.word)
        generate_embedding(keyword)
        print("Keyword embedding generated.")
        self.embedding_order.append(('keyword', keyword.id))
        self.total_keywords += 1

    def generate_keywords_embeddings(self, keywords: Dict[str, KeyWord]):
        for keyword in keywords.values():
            self.generate_keyword_embedding(keyword)

    def load_keywords(self, keyword_file_path: str):
        print("load_keywords called")
        self.keyword_objects = create_keyword_objects_from_txt(keyword_file_path)
        self.generate_keywords_embeddings(self.keyword_objects)
        print("load_keywords completed")
        print(f"Total keywords: {self.total_keywords}")

    def build_faiss_index(self):
        # We need to handle this differently if we are managing the document nodes and keywords separately
        embeddings = []
        print("Length of embedding_order before building the index:", len(self.embedding_order))
        for keyword in self.keyword_objects.values():
            embeddings.append(keyword.embedding)

        self.faiss_index = FaissIndex(embeddings)
        self.faiss_index.create_index()

    # We need to handle this differently if we are managing the document nodes and keywords separately
    def search_similar_nodes(self, query_embedding: List[float], k: int) -> Tuple[List[int], List[float]]:
        indices, distances = self.faiss_index.search(np.array([query_embedding]), k)
        return indices[0].tolist(), distances[0].tolist()

    def save_key_manager_state(self, output_directory: str): # Changed the name of this function to make it specific
        # to the key manager
        write_keywords_objects_to_file(self.keyword_objects, f"{output_directory}/keywords.txt")
        self.faiss_index.save_index(f"{output_directory}/faiss_index") # Need to figure out how this will work with the
        # new separate keyword manager

    def load_keyword_manager_state(self, input_directory: str):
        # self.document_nodes = read_document_nodes_from_file(f"{input_directory}/document_nodes.txt")
        self.keyword_objects = read_keyword_objects_from_file(f"{input_directory}/keywords.txt")

        # Clear the embedding order list
        self.embedding_order = []

        # Rebuild the embedding order list for keywords
        for keyword_id in self.keyword_objects:
            self.embedding_order.append(('keyword', keyword_id))

        # Loading the faiss index - need to decide what to do with this based on the new separate keyword manager
        self.faiss_index = FaissIndex([])
        self.faiss_index.load_index(f"{input_directory}/faiss_index")