import os
from lxml import etree
import docx
import tkinter as tk
from tkinter import filedialog

"""
This script removes the TOC from a .docx file and the associated header.
It prompts the user to select a .docx file using a file browser dialogue, and then
removes the TOC from the file and saves the modified file with the same name + "-noTOC" in the same directory.
"""


def remove_toc(doc_x):
    nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    xpath_toc = "//w:sdt/w:sdtPr/w:docPartObj/w:docPartGallery[@w:val='Table of Contents']"

    # Parse the XML tree
    xml_tree = etree.fromstring(doc_x.part.element.xml)

    # Find the TOC element
    toc_elements = xml_tree.xpath(xpath_toc, namespaces=nsmap)

    # Find the header element preceding the TOC, if it exists
    header_element = None
    if toc_elements:
        toc_element = toc_elements[0]
        toc_sdt = toc_element.getparent().getparent().getparent()
        prev_element = toc_sdt.getprevious()
        if prev_element is not None and prev_element.xpath("local-name()") == "p" and\
                prev_element.find("w:pPr/w:pStyle[@w:val='Heading1']", namespaces=nsmap) is not None:

            header_element = prev_element

        # Remove the TOC
        toc_sdt.getparent().remove(toc_sdt)

        # Remove the header element, if it exists
        if header_element is not None:
            header_element.clear()

        # Replace the 'w:body' element in the docx Document object with the modified one
        body_element = xml_tree.find("w:body", namespaces=nsmap)
        doc_x.part.element.body.clear()
        for child in body_element:
            doc_x.part.element.body.append(child)


if __name__ == "__main__":
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open a file browser dialogue and allow the user to select a .docx file
    file_path = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])

    # Load the .docx file
    doc = docx.Document(file_path)

    # Remove the TOC
    remove_toc(doc)

    # Save the modified document in the same directory as the original file, with a different name
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path).split(".")[0]
    doc.save(f"{file_dir}/{file_name}_noTOC.docx")
