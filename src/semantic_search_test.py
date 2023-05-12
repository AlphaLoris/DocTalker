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

    # doc_manager = DocumentManager()  # Assuming DocumentManager instance is already initialized with data

    output_path = file_path.replace(".txt", "_and_Neighbors.txt")

    # Iterate through the list of words
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for word in words:
            # Get an embedding for the current word
            embedding_response = get_embedding(word)
            # print(f"Embedding response for '{word}': {embedding_response}")  # Debug print statement
            embedding = embedding_response["data"][0]["embedding"]

            # Get the 7 nearest neighbors
            k = 7
            indices, distances = doc_manager.search_similar_nodes(embedding, k)

            # Write the word and neighbors to the output file
            # indices_list = indices[0]
            # distances_list = distances[0]

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
                        for sentence in node.create_sentence_list():
                            if sentence.id == text_object_id:
                                text_object = sentence
                                break
                        if text_object:
                            break
                    text = text_object.text
                elif embedding_type == 'keyword':
                    text_object = doc_manager.keyword_objects[text_object_id]
                    text = text_object.word

                output_file.write(f"\tNeighbor{i + 1} Text: {text}\n")
                output_file.write(f"\tNeighbor{i + 1} Distance: {distance}\n\n")

            output_file.write("=====================================\n\n")


if __name__ == "__main__":
    semantic_search_test(doc_manager=DocumentManager())
