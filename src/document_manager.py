# document_manager.py module

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
        self.embedding_order = []  # Add this line
        self.total_sentences = 0
        self.total_document_nodes = 0
        self.total_keywords = 0

    def load_documents(self, file_paths: List[str]):
        print("load_documents called")  # Add this line
        for file_path in file_paths:
            print("Parsing document: " + file_path)
            parser = DocxDocumentParser(file_path)
            print("Document parsed: " + file_path)
            nodes = parser.process_document()
            print("Returned from process_document() with nodes")
            # Error occurs here. The print statement below is not executed.
            for node_id, node in nodes.items():
                print("Generating node embedding for: " + node.body_text)
                generate_embedding(node)
                print("Node embedding generated.")
                self.total_document_nodes += 1
                self.embedding_order.append(('node', node_id))  # Add this line
                for sentence in node.create_sentence_list():
                    print("Generating sentence embedding for: " + sentence.text)
                    generate_embedding(sentence)
                    print("Sentence embedding generated.")
                    self.embedding_order.append(('sentence', sentence.id))  # Add this line
                    self.total_sentences += 1
            self.document_nodes.update(nodes)
        print("load_documents complete.")  # Add this line
        print(f"Total document nodes: {self.total_document_nodes}")
        print(f"Total sentences: {self.total_sentences}")

    def load_keywords(self, keyword_file_path: str):
        print("load_keywords called")  # Add this line
        self.keyword_objects = create_keyword_objects_from_txt(keyword_file_path)
        for keyword in self.keyword_objects.values():
            print("Generating keyword embedding for: " + keyword.word)
            generate_embedding(keyword)
            print("Keyword embedding generated.")
            self.embedding_order.append(('keyword', keyword.id))  # Add this line
            self.total_keywords += 1
        print("load_keywords completed")  # Add this line
        print(f"Total keywords: {self.total_keywords}")

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

