# document_manager.py module

from typing import List, Tuple
from src.docx_document_parser import DocxDocumentParser
from embeddings import create_keyword_objects_from_txt, generate_embedding, write_keywords_objects_to_file, \
    read_keyword_objects_from_file
from faiss_index import FaissIndex
from node import write_document_nodes_to_file, read_document_nodes_from_file


class DocumentManager:
    def __init__(self):
        self.document_nodes = {}
        self.keyword_objects = {}
        self.faiss_index = None

    def load_documents(self, file_paths: List[str]):
        for file_path in file_paths:
            parser = DocxDocumentParser(file_path)
            nodes = parser.process_document()
            for node_id, node in nodes.items():
                generate_embedding(node)
                for sentence in node.create_sentence_list():
                    generate_embedding(sentence)
            self.document_nodes.update(nodes)

    def load_keywords(self, keyword_file_path: str):
        self.keyword_objects = create_keyword_objects_from_txt(keyword_file_path)
        for keyword in self.keyword_objects.values():
            generate_embedding(keyword)

    def build_faiss_index(self):
        embeddings = []
        for node in self.document_nodes.values():
            embeddings.append(node.embedding)
            for sentence in node.create_sentence_list():
                embeddings.append(sentence.embedding)
        for keyword in self.keyword_objects.values():
            embeddings.append(keyword.embedding)

        self.faiss_index = FaissIndex(embeddings)
        self.faiss_index.create_index()

    def search_similar_nodes(self, query_embedding: List[float], k: int) -> Tuple[List[int], List[float]]:
        indices, distances = self.faiss_index.search(query_embedding, k)
        return indices, distances

    def save_manager_state(self, output_directory: str):
        write_document_nodes_to_file(self.document_nodes, f"{output_directory}/document_nodes.txt")
        write_keywords_objects_to_file(self.keyword_objects, f"{output_directory}/keywords.txt")
        self.faiss_index.save_index(f"{output_directory}/faiss_index")

    def load_manager_state(self, input_directory: str):
        self.document_nodes = read_document_nodes_from_file(f"{input_directory}/document_nodes.txt")
        self.keyword_objects = read_keyword_objects_from_file(f"{input_directory}/keywords.txt")
        self.faiss_index = FaissIndex([])
        self.faiss_index.load_index(f"{input_directory}/faiss_index")
