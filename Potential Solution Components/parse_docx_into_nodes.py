# parse_docx_into_nodes.py module

import sys
import os
import tkinter as tk
from tkinter import filedialog
from src.docx_document_parser import DocxDocumentParser
from src.embeddings import create_keyword_objects_from_txt, write_keywords_objects_to_file, read_keyword_objects_from_file, \
    generate_embedding
from src.node_old import read_document_nodes_from_file, write_document_nodes_to_file
import numpy as np

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize, edgeitems=sys.maxsize)


def select_file():
    doc_root = tk.Tk()
    doc_root.withdraw()
    doc_file_path = filedialog.askopenfilename(filetypes=[('Word Files', '*.docx')])
    return doc_file_path


if __name__ == '__main__':
    # Store the original stdout so you can reset it later
    original_stdout = sys.stdout
    try:
        # Open a file for writing and set sys.stdout to the file
        with open(r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments1\output.txt",
                  'w') as file:
            sys.stdout = file

            # Files
            nodes_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments1\Nodes.txt"
            keyword_objects_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments1\KeyWordObjects.txt"
            keyword_text_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\\Experiments\Experiments1\Key Words.txt"

            # Handle the nodes
            if os.path.exists(nodes_file_path):
                print("Reading nodes from file...")
                read_document_nodes_from_file(nodes_file_path)
            else:
                # Select a document to parse
                print("Select a document to parse...")
                word_file_path = select_file()
                if word_file_path:
                    # Create a DocxDocumentParser object and process the document to create a dictionary of nodes
                    document_parser = DocxDocumentParser(word_file_path)
                    print(f"Document title: {document_parser.document_title}")

                    # Create a dictionary of nodes based on the text contents of the document
                    print("Creating document nodes from text...")
                    document_nodes = document_parser.process_document()

                    # Generate embeddings for the document nodes and associate them with their respective document node
                    # objects
                    print("Generating embeddings for document nodes...")
                    for node in document_nodes.values():
                        generate_embedding(node)
                        print("Generating embeddings for sentences...")
                        for sentence in node.sentence_list:
                            generate_embedding(sentence)

                    # Write the document nodes with embeddings to a text file
                    output_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments1\Nodes.txt"
                    print(f"Output file path: {output_file_path}")
                    write_document_nodes_to_file(document_nodes, output_file_path)

            # Handle the keywords
            # Initialize keyword_list as an empty dictionary
            keyword_list = {}
            if os.path.exists(keyword_objects_file_path):
                print("Reading keyword objects from file...")
                keyword_list = read_keyword_objects_from_file(keyword_objects_file_path)
            else:
                if os.path.exists(keyword_text_file_path):
                    print("Creating keyword objects from text...")
                    keyword_list = create_keyword_objects_from_txt(keyword_text_file_path)

                    # Generate embeddings for the keywords and associate them with their respective keyword objects
                    print("Generating embeddings for keywords...")
                    for word in keyword_list.values():
                        generate_embedding(word)

                    # Write the keyword objects with embeddings to a text file
                    output_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments1\KeyWordObjects.txt"
                    write_keywords_objects_to_file(keyword_list, output_file_path)

            # Print the document_nodes and keyword objects to console
            for node in document_nodes.values():
                print(node.to_string())
            for word in keyword_list.values():
                print(word.to_string())

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout
