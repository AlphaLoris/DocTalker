import tkinter as tk
from tkinter import filedialog
from docx import Document
from pathlib import Path
from gpt_index import download_loader
from gpt_index.indices.prompt_helper import PromptHelper

"""
This script uses the gpt_index library to split a .docx file into chunks of text and save them to a .txt file. The
text splitter is oriented toward splitting the prompt, thus the name.
"""


class DataIngestion:
    def __init__(self):
        self.nodes = []
        # Initialize an instance of the PromptHelper class
        self.prompt_helper = PromptHelper(max_input_size=4096, num_output=1, max_chunk_overlap=200,
                                          embedding_limit=None, chunk_size_limit=None)
        self.prompt = ""

    def process_docx_files(self, docx_files):
        docx_reader = download_loader("DocxReader")
        loader = docx_reader()

        for docx_file in docx_files:
            documents = loader.load_data(file=Path(docx_file))
            prompt_length = 1000
            while prompt_length > 0:
                self.prompt = self.prompt + "x"
                prompt_length = prompt_length - 1
            # Get the text splitter
            text_splitter = self.prompt_helper.get_text_splitter_given_prompt(self.prompt, num_chunks=1)

            for document in documents:
                chunks = text_splitter.split_text(document)  # Split the document text into chunks
                self.nodes.extend(chunks)


# Script
def main():
    # Open a file browser and allow the user to select a .docx file
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
    if not file_path:
        print("No file selected. Exiting.")
        return

    # Read the .docx file and write its text to a new file with "-txt" appended to its file name
    doc = Document(file_path)
    txt_file_path = Path(file_path).with_name(Path(file_path).stem + "-txt.txt")
    # Write paragraphs to a file
    with open(txt_file_path, "w") as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(paragraph.text + "\n\n\n\n")

    # Parse the file into nodes and write the nodes to another file with "-nodes" appended to its file name
    data_ingestion = DataIngestion()
    data_ingestion.process_docx_files([file_path])

    # Write nodes to a file
    nodes_file_path = Path(file_path).with_name(Path(file_path).stem + "-prompt_helper_nodes.txt")
    with open(nodes_file_path, "w") as nodes_file:
        for node in data_ingestion.nodes:
            nodes_file.write(str(node) + "\n\n\n\n")

    print(f"Successfully processed {file_path}")


if __name__ == "__main__":
    main()
