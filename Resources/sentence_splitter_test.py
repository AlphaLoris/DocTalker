""" Sentence Splitter Test """

import tkinter as tk
from tkinter import filedialog
from docx import Document
from pathlib import Path
from gpt_index import download_loader
from gpt_index.node_parser.simple import SimpleNodeParser
from gpt_index.langchain_helpers.text_splitter import SentenceSplitter

"""
This script does pretty fine-grained sentence splitting on a .docx file. It uses the SentenceSplitter class from
langchain_helpers.text_splitter. It gives you control over chunk size and overlap, and allows you to specify the text
string it should split on.
"""

# TODO: figure out a way to leverage the chunk size and overlap controls and maybe the splitting methodology of this
#  script along with text_block_extractor.py to get the best of both worlds.

# Data Ingestion Class
class DataIngestion:
    def __init__(self):
        self.nodes = []

    def process_docx_files(self, docx_files):
        docx_reader = download_loader("DocxReader")
        loader = docx_reader()
        text_splitter = SentenceSplitter(
            separator=" ",
            chunk_size=1000,
            chunk_overlap=200,
            backup_separators=["\n", "\r"],
            paragraph_separator="\n\n",
            chunking_tokenizer_fn=None,
            secondary_chunking_regex="[^,.;]+[,.;]?"
        )
        node_parser = SimpleNodeParser(text_splitter=text_splitter, include_extra_info=True,
                                       include_prev_next_rel=True)
        for docx_file in docx_files:
            documents = loader.load_data(file=Path(docx_file))  # added self here. .
            nodes = node_parser.get_nodes_from_documents(documents)
            self.nodes.extend(nodes)


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

    with open(txt_file_path, "w") as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(paragraph.text + "\n")

    # Parse the file into nodes and write the nodes to another file with "-nodes" appended to its file name
    data_ingestion = DataIngestion()
    data_ingestion.process_docx_files([file_path])

    # Write nodes to a file
    nodes_file_path = Path(file_path).with_name(Path(file_path).stem + "-SentenceSplitter_nodes2.txt")
    with open(nodes_file_path, "w") as nodes_file:
        for node in data_ingestion.nodes:
            nodes_file.write(str(node) + "\n\n\n\n")
    print(f"Successfully processed {file_path}")


if __name__ == "__main__":
    main()
