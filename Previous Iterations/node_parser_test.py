"""
Node Parser Test

This parses a .docx file into a list of fairly large nodes, each of which is tagged with some info about its
relationship with the source document. Uses one of the node parsers from gpt_index.
"""

import tkinter as tk
from tkinter import filedialog
from docx import Document
from pathlib import Path
from gpt_index import download_loader
from gpt_index.node_parser.simple import SimpleNodeParser


# Data Ingestion Class
class DataIngestion:
    def __init__(self):
        self.nodes = []

    def process_docx_files(self, docx_files):
        docx_reader = download_loader("DocxReader")
        loader = docx_reader()
        node_parser = SimpleNodeParser()

        for docx_file in docx_files:
            documents = loader.load_data(file=Path(docx_file))  # added self here. .
            nodes = node_parser.get_nodes_from_documents(documents,)
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
    nodes_file_path = Path(file_path).with_name(Path(file_path).stem + "-node_parser_nodes.txt")
    with open(nodes_file_path, "w") as nodes_file:
        for node in data_ingestion.nodes:
            nodes_file.write(str(node) + "\n\n\n\n")
    print(f"Successfully processed {file_path}")


if __name__ == "__main__":
    main()
