"""
document_manager.py Module

This module provides a DocumentManager class for managing documents, the related embeddings, and Faiss indexing. The
DocumentManager class handles document parsing, embedding generation, Faiss index building, and
saving/loading of manager state.

Usage:
1. Create an instance of the DocumentManager class.
2. Use the provided methods to load documents, build the Faiss index, search for similar nodes, and
save/load the manager state.

Dependencies:
- List, Tuple from typing
- DocxDocumentParser from utils.docx_document_parser
- generate_embedding
- FaissIndex from faiss_index
- np from numpy

Notes:
- The DocumentManager class tracks document nodes, Faiss index, embedding order, and statistics.
- The load_documents method parses and processes document files, generating embeddings for nodes and sentences.
- The build_faiss_index method builds the Faiss index using document and sentence embeddings.
- The search_similar_nodes method performs a search using a query embedding and returns similar nodes.
- The save_manager_state method saves document nodes and the Faiss index to files.
- The load_manager_state method loads document nodes and the Faiss index from files, and rebuilds the embeddings and
their order.
"""

from typing import Dict
from utils.docx_document_parser import Document
from node import DocumentNode
from typing import List, Tuple
from utils.docx_document_parser import DocxDocumentParser
from embeddings import generate_embedding
from faiss_index import FaissIndex
from node import write_document_nodes_to_file, read_document_nodes_from_file
import numpy as np
import math
import json


class DocumentManager:
    def __init__(self):
        self.document_nodes = {}
        self.faiss_indexes = {'node': None, 'sentence': None}  # Separate FaissIndex instances
        self.embedding_order = {'node': [], 'sentence': []}  # Separate lists for nodes and sentences
        self.total_sentences = 0
        self.total_document_nodes = 0

    def create_docx_files_dictionary(self, file_paths: List[str]) -> Dict[str, Document]:
        documents = {}
        # Creates a dictionary of docx files with the file path as the key and the document as the value
        print("Creating a dictionary of document parsers for the documents in the selected directory")
        for file_path in file_paths:
            print("Creating document parser for: " + file_path)
            parser = DocxDocumentParser(file_path)
            print("Document loaded: " + file_path)
            documents[file_path] = parser
        return documents

    def load_documents(self, file_paths: List[str]):
        print("load_documents called")
        documents = self.create_docx_files_dictionary(file_paths)
        doc_nodes = self.process_documents(documents)
        self.generate_embeddings(doc_nodes)
        self.update_document_nodes(doc_nodes)
        print("load_documents complete.")
        print(f"Total document nodes: {self.total_document_nodes}")
        print(f"Total sentences: {self.total_sentences}")

    def process_documents(self, documents: Dict[str, Document]) -> Dict[str, Dict[str, DocumentNode]]:
        # Convert each document loaded in into a set of nodes using its DocxDocumentParser and add its nodes dictionary
        nodes = {}
        for file_path, document in documents.items():
            print("Processing document into nodes: " + file_path)
            document_nodes = document.process_document()
            nodes[file_path] = document_nodes  # document_nodes should be a dict[str, DocumentNode]
            print("Document processed into nodes: " + file_path)
        return nodes

    def update_document_nodes(self, nodes: Dict[str, Dict[str, DocumentNode]]):
        # Update the document_nodes dictionary with the nodes from the set of loaded documents
        for file_path, node_dict in nodes.items():
            self.document_nodes.update(node_dict)

    def generate_embeddings(self, nodes: Dict[str, Dict[str, DocumentNode]]):
        # Generate embeddings for each node and sentence in the set of loaded documents
        # We may want to make this configurable to allow for control over which embeddings are generated
        self.generate_node_embeddings(nodes)
        self.generate_sentence_embeddings(nodes)

    def generate_node_embeddings(self, nodes: Dict[str, Dict[str, DocumentNode]]):
        for file_path, node_dict in nodes.items():
            for node_id, node in node_dict.items():
                print("Generating node embedding for: " + node.body_text)
                generate_embedding(node)
                print("Node embedding generated.")
                self.embedding_order['node'].append(('node', node_id))
                self.total_document_nodes += 1

    def generate_sentence_embeddings(self, nodes: Dict[str, Dict[str, DocumentNode]]):
        for file_path, node_dict in nodes.items():
            for node_id, node in node_dict.items():
                for sentence in node.sentence_list:  # Access the sentence_list directly
                    print("Generating sentence embedding for: " + sentence.text)
                    generate_embedding(sentence)
                    print("Sentence embedding generated.")
                    self.embedding_order['sentence'].append(('sentence', sentence.id))
                    self.total_sentences += 1

    def save_nodes_body_text(self, file_path):
        # Create a .txt file to save all the node body text values
        with open(file_path, 'w') as f:
            for node in self.document_nodes.values():
                f.write(node.body_text + '\n')

    def save_sentence_text(self, file_path):
        with open(file_path, 'w') as f:
            for node in self.document_nodes.values():
                for sentence in node.sentence_list:
                    f.write(sentence.text + '\n')

    def print_first_five_words_of_nodes(self):
        for node_id, node in self.document_nodes.items():
            # split the body text into words
            words = node.body_text.split()

            # get the first five words
            first_five_words = words[:5]

            # join the words back into a string
            first_five_words_str = ' '.join(first_five_words)

            # print the ID and the first five words
            print(f'{node_id} : {first_five_words_str}')

    def print_embedding_order(self):
        for data_type in ['node', 'sentence']:
            print(f"Embedding order for {data_type}s:")
            for embedding_type, id in self.embedding_order[data_type]:
                print(f"{embedding_type} ID: {id}\n")

    def build_faiss_index(self):
        for data_type in ['node', 'sentence']:
            embeddings = []
            print(f"Length of {data_type} embedding_order before building the index:",
                  len(self.embedding_order[data_type]))
            for embedding_type, id in self.embedding_order[data_type]:
                if embedding_type == 'node':
                    embeddings.append(self.document_nodes[id].embedding)
                else:  # embedding_type == 'sentence'
                    for node in self.document_nodes.values():
                        for sentence in node.sentence_list:
                            if sentence.id == id:
                                embeddings.append(sentence.embedding)
                                break
            self.faiss_indexes[data_type] = FaissIndex(embeddings, data_type)
            # calculate the index nlist and nprobe values
            nlist = int(math.sqrt(len(embeddings)))
            nprobe = nlist  # nprobe should be equal to nlist for best performance when the number of embeddings is
            # small
            self.faiss_indexes[data_type].create_index(nlist, nprobe)

    def search_similar_nodes(self, query_embedding: List[float], k: int, data_type='node') -> \
            Tuple[List[int], List[float]]:
        # print("self.faiss_indexes[datatype]" + self.faiss_indexes[data_type])
        indices, distances = self.faiss_indexes[data_type].search(np.array([query_embedding]), k)
        return indices[0].tolist(), distances[0].tolist()

    def save_manager_state(self, output_directory: str):
        write_document_nodes_to_file(self.document_nodes, f"{output_directory}/document_nodes.txt")
        for data_type in ['node', 'sentence']:
            self.faiss_indexes[data_type].save_index(f"{output_directory}/faiss_index_{data_type}")
        # Save the embedding_order
        with open(f"{output_directory}/embedding_order.json", 'w') as f:
            json.dump(self.embedding_order, f)

    def load_manager_state(self, input_directory: str):
        self.document_nodes = read_document_nodes_from_file(f"{input_directory}/document_nodes.txt")
        # Load the embedding_order
        with open(f"{input_directory}/embedding_order.json", 'r') as f:
            self.embedding_order = json.load(f)
        embeddings = {'node': [], 'sentence': []}
        for embedding_type, id in self.embedding_order['node']:
            embeddings['node'].append(self.document_nodes[id].embedding)
        for embedding_type, id in self.embedding_order['sentence']:
            # find the sentence with the given id
            for node in self.document_nodes.values():
                for sentence in node.create_sentence_list():
                    if sentence.id == id:
                        embeddings['sentence'].append(sentence.embedding)
                        break
        for data_type in ['node', 'sentence']:
            self.faiss_indexes[data_type] = FaissIndex(embeddings[data_type], data_type)
            self.faiss_indexes[data_type].load_index(f"{input_directory}/faiss_index_{data_type}")
