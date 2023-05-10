import zipfile
import os
import tkinter as tk
from tkinter import filedialog

"""
This script extracts all the files and resources from a .docx file.
It prompts the user to select a .docx file using a file browser dialogue, and then
saves the extracted files to a new directory with the same name as the input file.
"""


def extract_docx_files(docx_path):
    # Create the output directory with the same name as the input file
    file_name, file_ext = os.path.splitext(docx_path)
    output_dir = f'{file_name}-unzipped'
    os.makedirs(output_dir, exist_ok=True)

    # Extract all the files from the .docx file to the output directory
    with zipfile.ZipFile(docx_path, 'r') as docx_file:
        docx_file.extractall(output_dir)

    return output_dir


if __name__ == "__main__":
    # Create a Tkinter root window to open the file browser dialogue
    root = tk.Tk()
    root.withdraw()

    # Open the file browser dialogue to select a .docx file
    file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])
    if file_path:
        output_directory = extract_docx_files(file_path)
        print(f"File successfully unzipped and files saved in the directory: {output_directory}")
