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


def semantic_search_test(doc_manager):
    # Launch a Windows file browser and get the .txt file path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    # Load words from the text file
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()

    output_path = file_path.replace(".txt", "_and_Neighbors.txt")

    # Iterate through the list of words
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for word in words:
            # Get an embedding for the current word
            embedding_response = get_embedding(word)
            # print(f"Embedding response for '{word}': {embedding_response}")
            embedding = embedding_response["data"][0]["embedding"]

            # Get the 7 nearest neighbors
            k = 7
            indices, distances = doc_manager.search_similar_nodes(embedding, k)

            # Write the word and neighbors to the output file
            output_file.write(f"Word: {word}\n")
            for i, (index, distance) in enumerate(zip(indices, distances)):
                index = int(index)  # Convert index to integer
                print("Indices:", indices)
                print("Length of embedding_order:", len(doc_manager.embedding_order))
                embedding_type, text_object_id = doc_manager.embedding_order[index]

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
                        output_file.write(f"\tNeighbor{i + 1} ID: {text_object_id}\n")
                elif embedding_type == 'keyword':
                    text_object = doc_manager.keyword_objects[text_object_id]
                    text = text_object.word

                output_file.write(f"\tNeighbor{i + 1} ID: {text_object_id}\n")
                output_file.write(f"\tNeighbor{i + 1} Text: {text}\n")
                output_file.write(f"\tNeighbor{i + 1} Distance: {distance}\n\n")

            output_file.write("=====================================\n\n")


if __name__ == "__main__":
    semantic_search_test(doc_manager=DocumentManager())

""" Original copy of elif statement above
elif embedding_type == 'sentence':
    text_object = None
    for node in doc_manager.document_nodes.values():
        for sentence in node.create_sentence_list():
            if sentence.id == text_object_id:
                print("Sentence Text:", sentence.text)
                text_object = sentence
                break
        if text_object:
            break
    text = text_object.text
"""
