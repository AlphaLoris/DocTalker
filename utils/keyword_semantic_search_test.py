# keyword_semantic_search_test.py module

"""
keyword_semantic_search_test.py

This module provides a function for performing semantic search using word embeddings. It takes a DocumentManager
instance as input and performs semantic search on a list of words obtained from a user-selected text file. The function
finds the nearest neighbors of each word in the document corpus and outputs the results to a file.

Usage:
    1. Execute the module to run the semantic search test.
    2. A file dialog will prompt for a text file containing words to search.
    3. The DocumentManager instance should be already initialized with document data.
    4. The nearest neighbors of each word will be found using word embeddings.
    5. The results will be written to an output file, including the word and its neighbors.

Dependencies:
    - tkinter as tk
    - filedialog from tkinter
    - embeddings from embeddings
    - DocumentManager from document_manager

Notes:
    - This module assumes that the DocumentManager instance is already initialized with document data.
    - The user needs to select a text file containing words to search.
    - The output file will have a similar name as the input file with "_and_Neighbors" appended.
    - The number of nearest neighbors to find is set to 7 by default.
"""

import tkinter as tk
from tkinter import filedialog
from embeddings import get_embedding
from document_manager import DocumentManager
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)


def semantic_search_test(doc_manager, data_type='node'):  # default is 'node'
    logger.debug("Starting semantic search test.")
    # Launch a Windows file browser and get the .txt file path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    logger.info("Loading words from %s.", file_path)

    # Load words from the text file
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()

    output_path = file_path.replace(".txt", "_and_Neighbors.txt")
    logger.info("Writing results to %s.", output_path)

    # Iterate through the list of words
    logger.info("Performing semantic search on %d words.", len(words))
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for word in words:
            # Get an embedding for the current word
            embedding_response = get_embedding(word)
            embedding = embedding_response["data"][0]["embedding"]

            # Get the 7 nearest neighbors
            logger.info("Finding the k nearest neighbors for %s.", word)
            k = 7
            indices, distances = doc_manager.search_similar_nodes(embedding, k, data_type)

            # Write the word and neighbors to the output file
            logger.info("Writing results to %s.", output_path)
            output_file.write(f"Word: {word}\n")
            for i, (index, distance) in enumerate(zip(indices, distances)):
                index = int(index)  # Convert index to integer
                print("Indices:", indices)
                print("Length of embedding_order[node]:", len(doc_manager.embedding_order['node']))
                print("Length of embedding_order[sentence]:", len(doc_manager.embedding_order['sentence']))

                if data_type == 'node':
                    print("Node Embedding order:", doc_manager.embedding_order['node'][index])
                    embedding_type, text_object_id = doc_manager.embedding_order['node'][index]
                elif data_type == 'sentence':
                    print("Sentence Embedding order:", doc_manager.embedding_order['sentence'][index])
                    embedding_type, text_object_id = doc_manager.embedding_order['sentence'][index]

                if embedding_type == 'node':
                    text_object = doc_manager.document_nodes[text_object_id]
                    text = text_object.body_text
                elif embedding_type == 'sentence':
                    text_object = None
                    for node in doc_manager.document_nodes.values():
                        for sentence in node.sentence_list:  # Use the stored sentence list
                            if sentence.id == text_object_id:
                                print("Sentence Text:", sentence.text)
                                text_object = sentence
                                break
                        if text_object:
                            break
                    if text_object is None:
                        print(f"No sentence found with id {text_object_id}.")
                        output_file.write(f"\tNeighbor{i + 1} ID: {text_object_id} (NOT FOUND)\n")
                        text = ""
                    else:
                        text = text_object.text
                        # output_file.write(f"\tNeighbor{i + 1} ID: {text_object_id}\n")
                elif embedding_type == 'keyword':
                    text_object = doc_manager.keyword_objects[text_object_id]
                    text = text_object.word

                output_file.write(f"\tNeighbor{i + 1} ID: {text_object_id}\n")
                output_file.write(f"\tNeighbor{i + 1} Text: {text}\n")
                output_file.write(f"\tNeighbor{i + 1} Distance: {distance}\n\n")

            output_file.write("=====================================\n\n")
            logger.debug("Finished semantic search test.")


if __name__ == "__main__":
    logger.debug("Launching semantic search test.")
    semantic_search_test(doc_manager=DocumentManager())
