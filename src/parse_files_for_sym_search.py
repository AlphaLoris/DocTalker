# parse_files_for_sym_search.py module

import sys
import os
import tkinter as tk
from tkinter import filedialog
from document_manager import DocumentManager
import numpy as np
from semantic_search_test import semantic_search_test

# TODO: Optimizations
# TODO: Add a progress bar for document upload and parsing/embedding
# TODO: Optimize text division
# TODO: Optimize Index type
# TODO: Optimize Similarity calculation type
# TODO: Optimize number of results returned
# TODO: Optimize method of assembling results into prompt
# TODO: Optimize prompt composition/characteristics/technique
# TODO: Optimize response validation

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

            # Files
            nodes_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\Nodes.txt"
            keyword_objects_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\Experiments\Experiments2\KeyWordObjects.txt"
            keyword_text_file_path = r"c:\Users\glenn\OneDrive\Documents\Glenn's Docs\Linklings\WIP\\Experiments\Experiments2\Key Words.txt"

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
                    doc_manager.load_documents([word_file_path])

                    # Handle the keywords
                    if os.path.exists(keyword_text_file_path):
                        print("Loading keywords...")
                        doc_manager.load_keywords(keyword_text_file_path)

                    # Build Faiss index
                    print("Building Faiss index...")
                    doc_manager.build_faiss_index()

                    # Save manager state to files
                    print("Saving manager state to files...")
                    output_directory = os.path.dirname(nodes_file_path)
                    doc_manager.save_manager_state(output_directory)

            semantic_search_test()

            # Print the document_nodes and keyword objects to console
            for node in doc_manager.document_nodes.values():
                print(node.to_string())
            for word in doc_manager.keyword_objects.values():
                print(word.to_string())

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout
