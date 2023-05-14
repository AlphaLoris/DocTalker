"""
keyword_manager.py Module

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

from typing import Dict, Optional
from typing import List, Tuple
from faiss_index import FaissIndex
from embeddings import KeyWord, create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file, \
    read_keyword_objects_from_file
import numpy as np


class KeywordManager:
    def __init__(self):
        self.keyword_objects = {}
        self.faiss_indexes: Dict[str, Optional[FaissIndex]] = {'keyword': None}  # Separate FaissIndex instances
        self.embedding_order = {'keyword': []}  # Separate list for keywords
        self.total_keywords = 0

    def generate_keyword_embedding(self, keyword: KeyWord):
        print("Generating keyword embedding for: " + keyword.word)
        generate_embedding(keyword)
        print("Keyword embedding generated.")
        self.total_keywords += 1
        self.embedding_order['keyword'].append(('keyword', keyword.id))

    def load_keywords(self, keyword_file_path: str):
        print("load_keywords called")
        self.keyword_objects = create_keyword_objects_from_txt(keyword_file_path)
        for keyword in self.keyword_objects.values():
            self.generate_keyword_embedding(keyword)
        print("load_keywords completed")
        print(f"Total keywords: {self.total_keywords}")

    def build_faiss_index(self):
        embeddings = []
        print("Length of keyword embedding_order before building the index:", len(self.embedding_order['keyword']))
        for _, id in self.embedding_order['keyword']:
            embeddings.append(self.keyword_objects[id].embedding)
        self.faiss_indexes['keyword'] = FaissIndex(embeddings, 'keyword')
        self.faiss_indexes['keyword'].create_index()

    def search_similar_keywords(self, query_embedding: List[float], k: int) -> Tuple[List[int], List[float]]:
        indices, distances = self.faiss_indexes['keyword'].search(np.array([query_embedding]), k)
        return indices[0].tolist(), distances[0].tolist()

    def save_manager_state(self, output_directory: str):
        write_keywords_objects_to_file(self.keyword_objects, f"{output_directory}/keywords.txt")
        self.faiss_indexes['keyword'].save_index(f"{output_directory}/faiss_index_keyword")

    def load_manager_state(self, input_directory: str):
        self.keyword_objects = read_keyword_objects_from_file(f"{input_directory}/keywords.txt")

        # Clear the embedding order list
        self.embedding_order['keyword'] = []

        # Rebuild the embeddings and their order
        embeddings = []
        for keyword_id, keyword in self.keyword_objects.items():
            self.embedding_order['keyword'].append(('keyword', keyword_id))
            embeddings.append(keyword.embedding)

        # Loading the faiss index
        self.faiss_indexes['keyword'] = FaissIndex(embeddings, 'keyword')
        self.faiss_indexes['keyword'].load_index(f"{input_directory}/faiss_index_keyword")
