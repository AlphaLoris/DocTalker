import zipfile
from lxml import etree
import tkinter as tk
from tkinter import filedialog

"""
This script extracts the text elements from a .docx file using the <w:t> tag, composes them into natural
blocks of text and saves them to a .txt file, with the role of each block (e.g. Title, Heading 1, Body, etc.)
indicated at the beginning of each block.
"""

# TODO: figure out how this is treating bulleted lists and numbered lists and any other special cases.


def unzip_docx(file_path):
    with zipfile.ZipFile(file_path, 'r') as docx_zip:
        document_xml = docx_zip.read('word/document.xml')
    return document_xml


def parse_document_xml(document_xml):
    return etree.fromstring(document_xml)


def extract_text_elements_with_role(root):
    paragraphs = root.findall('.//w:p', root.nsmap)
    text_contents_with_role = []
    current_role = None
    current_text = ""

    for paragraph in paragraphs:
        paragraph_style = paragraph.find('.//w:pPr/w:pStyle', root.nsmap)
        style = paragraph_style.get(f'{{{root.nsmap["w"]}}}val') if paragraph_style is not None else 'Body'

        text_elements = paragraph.findall('.//w:t', root.nsmap)

        for text_element in text_elements:
            text_content = text_element.text

            if current_role is None:
                current_role = style
                current_text = text_content
            elif current_role == style:
                current_text += " " + text_content
            else:
                text_contents_with_role.append((current_role, current_text))
                current_role = style
                current_text = text_content

    # Append the last block of text
    if current_text:
        text_contents_with_role.append((current_role, current_text))

    return text_contents_with_role


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Word Files', '*.docx')])
    return file_path


def save_to_txt(text_contents_with_role, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for role, text_content in text_contents_with_role:
            output_file.write(f'{role}: {text_content}\n')


if __name__ == '__main__':
    file_path = select_file()

    if file_path:
        document_xml = unzip_docx(file_path)
        root = parse_document_xml(document_xml)
        text_contents_with_role = extract_text_elements_with_role(root)

        output_file_path = file_path.replace('.docx', '-text_blocks_with_role.txt')
        save_to_txt(text_contents_with_role, output_file_path)
        print(f'Text elements with role saved to: {output_file_path}')
    else:
        print('No file selected.')
