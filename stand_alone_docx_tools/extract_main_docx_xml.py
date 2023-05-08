import zipfile
import os
import tkinter as tk
from tkinter import filedialog

"""
This script extracts the main document XML file (document.xml) from a .docx file.
It prompts the user to select a .docx file using a file browser dialogue, and then 
saves the extracted XML to a file with the same name + "-xml" in the same directory.
"""


def extract_docx_xml(docx_path):
    # Extract the main document XML file (document.xml) from the .docx file
    with zipfile.ZipFile(docx_path, 'r') as docx_file:
        document_xml = docx_file.read('word/document.xml')

    # Create the output file path by appending '-xml.xml' to the input file name
    file_name, file_ext = os.path.splitext(docx_path)
    output_file_path = f'{file_name}-xml.xml'

    # Save the extracted XML to the output file in the same directory
    with open(output_file_path, 'wb') as output_file:
        output_file.write(document_xml)


if __name__ == "__main__":
    # Create a Tkinter root window to open the file browser dialogue
    root = tk.Tk()
    root.withdraw()

    # Open the file browser dialogue to select a .docx file
    file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])
    if file_path:
        extract_docx_xml(file_path)
        print("File successfully unzipped and XML saved in the same directory.")
