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


# TODO: Understand commercial licensing requirements for resources used in this project
# TODO: Maybe use Faiss w/o GPU support and w/o Conda
# TODO: Analyze code with Pylint, Pydeps and mypy, radon or wily
# TODO: Understand the legal requirements for using the OpenAI API
# TODO: Optimizations
# TODO: Optimize text division
# TODO: Optimize Index type
# TODO: Optimize Similarity calculation type
# TODO: Optimize number of results returned
# TODO: Optimize method of assembling results into prompt
# TODO: Optimize prompt composition/characteristics/technique
# TODO: Optimize response validation
# TODO: Develop ways to evaluate and understand the semantic search performance
# TODO: Develop ways to understand the relative characteristics of the embeddings
# TODO: Include headings in the chunk text
# TODO: Page Numbers are not working. Would need to develop a new approach to parsing .docx files to get page numbers.
# TODO: Tune nlist and nprobe for Faiss index
# TODO: Add docstrings to the components
# TODO: Add Logging to the components
# TODO: Add unit tests to the components
# TODO: Backup of all Data
# TODO: Expose all behavioral parameters to the user: Model parameters, Tokenizer parameters, error checking, etc.
# TODO: Capture the questions the model had trouble answering and use them to improve the documentation
# TODO: Use a visual representation tool like Nomic to map queries against the user manual content to identify problem
#  areas
# TODO: Add a setup wizard that sets up the environment and configures the application
# TODO: Remove the OPENAI API KEY from the code and use a config file instead
# TODO: Semantic search review/maintenance interface
# TODO: Document Management interface
#  1. Add new documents
#  2. Remove documents
#  3. Backing up of data - Directory, primary/secondary backup versions
#  4. Restore previous state from backup
#  3. Progress bar for document upload, parsing/embedding, indexing
#  4. Control over number of neighbors returned and included in the prompt
#  5. Control over the prompt composition/characteristics/technique
#  6. Startup/Shutdown Chat

# TODO: Configuration
#   1. Model parameters: Model, temperature, top_p, n, stream, max_tokens, presence_penalty, frequency_penalty
#   2. Allow the admin user to choose the level of error checking
#   3. n_list, nprobe parameters for Faiss

# TODO: Chatbot Interface Features
#  1. Text entry box
#  2. Send button
#  3. Chat history window
#  4. Scroll the chat history window
#  1. Start new chat session - Drops chat history

# TODO: Features of Chatbot:
#  1. Control over chat session Start/Restart; End/Delete
#  2. History of Chat sessions
#  3. Responsive to the user's mood/emotional state
#  4. Ability to save/export the chat session to file and maybe email
#  5. Personalization of the chatbot based on the user's name, role, conference, etc.
#  6. Memory of previous conversations with User
#  7. Access to previous chat sessions
#  8. Chat session introduction
#       - Alert User that they are talking to an AI chatbot
#       - Alert User that the chatbot is trained on the User Manual
#       - Tell user how to reach a human
#  9. Alert User when the chatbot is not confident about the answer
#  10. Access to other means of communicating with humans for support
#  11. Ability to ask the User to provide feedback on individual answers
#  12. Ability to ask the User to provide feedback on the chatbot session as a whole
#  10. Scrolling chat window
#  18. Jump to the top/bottom of the chat window
#  11. Complex user input: Multiple sentences, paragraphs, carriage returns etc.
#  12. Paste into the chat session
#  11. Copy out of the chat window with visual indication of selected text
#  12. Visual differentiation of chatbot responses from User input
#  15. Give the user control over the size of the text in the chat window
#  16. Streaming chat w typing indicator
#  17. Answers should provide reference to the User Manual section/page number
#  18. View current Chat AI Context (the chat history provided as part of the prompt to the AI)


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
