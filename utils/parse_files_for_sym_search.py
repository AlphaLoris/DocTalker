"""
parse_files_for_sym_search.py Module --This module exercises all the document parsing and semantic search functionality

This module provides functionality for parsing and analyzing documents for semantic search. It uses the DocumentManager
class to handle document loading, keyword extraction, indexing, and saving/loading of manager state. The module also
includes a function for performing a semantic search test using the provided DocumentManager.

Usage:
    1. Execute the module to perform the document parsing and semantic search test.
    2. The module will prompt for a document file to parse and load.
    3. The parsed documents will be processed and indexed using the DocumentManager.
    4. If manager state files exist, they will be loaded; otherwise, new documents and keywords will be processed.
    5. The Faiss index will be built based on the processed documents.
    6. Manager state files will be saved for future use.
    7. Finally, a semantic search test will be performed, providing search results.

Dependencies:
    - sys
    - os
    - tkinter
    - filedialog from tkinter
    - DocumentManager from document_manager
    - numpy as np
    - semantic_search_test from keyword_semantic_search_test
"""

#  Conda Virtual Environment: C:\Users\glenn\anaconda3\envs\doc_talker_faiss

import sys
import os
import tkinter as tk
from tkinter import filedialog
from document_manager import DocumentManager
from keyword_manager import KeywordManager
import numpy as np
from keyword_semantic_search_test import semantic_search_test
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)

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
        with open(r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\output.txt",
                  'w') as file:
            sys.stdout = file

            # Initialize DocumentManager
            doc_manager = DocumentManager()
            # Initialize KeywordManager
            keywrd_manager = KeywordManager()

            # Files
            nodes_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\document_nodes.txt"
            keyword_objects_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\keywords.txt"
            keyword_text_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\\Experiments\Experiments2\Key Words.txt"
            nodes_txt_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\document_nodes_body_text.txt"
            sentences_txt_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\sentences.txt"

            # Handle the nodes
            if os.path.exists(nodes_file_path):
                print("Loading manager state from files...")
                doc_manager.load_manager_state(os.path.dirname(nodes_file_path))
            else:
                # Select a document to parse
                print("Select a document to parse...")
                word_file_path = select_file()
                if word_file_path:
                    # Load documents
                    print("Loading documents...")
                    doc_manager.load_documents([word_file_path])
                    print("Number of document nodes:", len(doc_manager.document_nodes))
                    print("Done loading documents.")

                    # Handle the keywords
                    if os.path.exists(keyword_text_file_path):
                        print("Loading keywords...")
                        keywrd_manager.load_keywords(keyword_text_file_path)
                        print("Number of keyword objects:", len(keywrd_manager.keyword_objects))
                        print("Done loading keywords.")

                    # Write the document_nodes dictionary to the console
                    doc_manager.print_first_five_words_of_nodes()

                    # Write the embedding order dictionary to the console
                    doc_manager.print_embedding_order()

                    # Build Faiss index
                    print("Building Faiss index...")
                    doc_manager.build_faiss_index()
                    print("Done building Faiss index.")

                    # Save manager state to files
                    print("Saving manager state to files...")
                    output_directory = os.path.dirname(nodes_file_path)
                    doc_manager.save_manager_state(output_directory)
                    print("Done saving manager state to files.")

            doc_manager.print_embedding_order()
            semantic_search_test(doc_manager, data_type='node')  # to search the 'node' index
            # or
            # semantic_search_test(doc_manager, data_type='sentence')  # to search the 'sentence' index

            # Write the document_nodes body_text a file
            doc_manager.save_nodes_body_text(nodes_txt_file_path)

            # Write the sentences text to a file
            doc_manager.save_sentence_text(sentences_txt_file_path)

            # Print the document_nodes and keyword objects to console
            for node in doc_manager.document_nodes.values():
                print(node.to_string())
            for word in keywrd_manager.keyword_objects.values():
                print(word.to_string())

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout
