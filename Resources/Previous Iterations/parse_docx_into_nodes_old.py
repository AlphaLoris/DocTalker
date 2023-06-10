import zipfile
from lxml import etree
import tkinter as tk
from tkinter import filedialog
import uuid
import re
from typing import List

"""
This version handles the body text correctly, and handles the headings correctly. It does not currently capture a title.
"""

def remove_toc(xml_tree):
    nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    xpath_toc = "//w:sdt/w:sdtPr/w:docPartObj/w:docPartGallery[@w:val='Table of Contents']"

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
            header_element.getparent().remove(header_element)


def generate_unique_id():
    return str(uuid.uuid4())


def unzip_docx(file_path):
    with zipfile.ZipFile(file_path, 'r') as docx_zip:
        document_xml = docx_zip.read('word/document.xml')
    return document_xml


def parse_document_xml(document_xml):
    return etree.fromstring(document_xml)


def condense_blank_lines(xml):
    namespaces = xml.nsmap
    paragraphs = xml.findall(".//w:p", namespaces)
    remove_elements = []
    last_was_blank = False

    for p in paragraphs:
        is_blank = not p.text and not any(elem.text for elem in p.iter())
        spacing = p.find(".//w:spacing", namespaces)

        if is_blank and last_was_blank:
            remove_elements.append(p)
        else:
            last_was_blank = is_blank
            if is_blank and spacing is not None:
                spacing.set(f'{{{namespaces["w"]}}}before', '0')
                spacing.set(f'{{{namespaces["w"]}}}after', '0')

    for elem in remove_elements:
        elem.getparent().remove(elem)


def extract_text_elements(root):
    paragraphs = root.findall('.//w:p', root.nsmap)
    text_contents = []
    current_headings = []

    for paragraph in paragraphs:
        paragraph_style = paragraph.find('.//w:pPr/w:pStyle', root.nsmap)
        style = paragraph_style.get(f'{{{root.nsmap["w"]}}}val') if paragraph_style is not None else 'Body'
        runs = paragraph.findall('.//w:r', root.nsmap)
        current_text = ""

        for run in runs:
            text_elements = run.findall('.//w:t', root.nsmap)
            line_breaks = run.findall('.//w:br', root.nsmap)

            for text_element in text_elements:
                text_content = text_element.text
                current_text += text_content

            if line_breaks:
                current_text += "\n"

        if "Heading" in style:
            heading_level = int(style[-1])
            if len(current_headings) >= heading_level:
                current_headings = current_headings[:heading_level - 1]
            current_headings.append(current_text.strip())

            if text_contents and text_contents[-1][0] == "Body":
                text_contents[-1] = ("Body", text_contents[-1][1] + "\n" + current_text.strip(),
                                     current_headings.copy())
            else:
                text_contents.append(("Body", current_text.strip(), current_headings.copy()))
            text_contents.append((style, "", []))
        else:
            if text_contents and text_contents[-1][0] == "Body":
                text_contents[-1] = ("Body", text_contents[-1][1] + "\n" + current_text.strip(),
                                     current_headings.copy())
            else:
                text_contents.append(("Body", current_text.strip(), current_headings.copy()))

    return text_contents


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Word Files', '*.docx')])
    return file_path


class DocumentNode:
    def __init__(self, title, headings, body_text, prev_node=None, next_node=None):
        self.id = generate_unique_id()
        self.title = title
        self.headings = headings
        self.body_text = body_text
        self.prev_node = prev_node
        self.next_node = next_node
        self.sentence_list = self.create_sentence_list()

    def create_sentence_list(self) -> List['Sentence']:
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', self.body_text)
        sentence_objects = []
        for i, sentence_text in enumerate(sentences):
            prev_sentence = sentence_objects[-1].id if i > 0 else None
            sentence = SentenceFactory.create_sentence(text=sentence_text, prev_sentence=prev_sentence)
            sentence_objects.append(sentence)
            if i > 0:
                sentence_objects[i - 1].next_sentence = sentence.id
        return sentence_objects

    def to_string(self):
        result = ""
        result += "id:\n" + str(self.id) + "\n\n"
        result += "title:\n" + self.title + "\n\n"
        result += "headings:\n" + self.headings + "\n\n"
        result += "body_text:\n" + self.body_text + "\n\n"
        result += "prev_node:\n" + str(self.prev_node) + "\n\n"
        result += "next_node:\n" + str(self.next_node) + "\n\n"
        # result += "sentence_list:\n" + "\n".join([sentence.to_string() for sentence in self.sentence_list]) + "\n\n"
        result += "\n"
        return result


class Sentence:
    def __init__(self, id, text, prev_sentence=None, next_sentence=None):
        self.id = id
        self.text = text
        self.prev_sentence = prev_sentence
        self.next_sentence = next_sentence

    def to_string(self):
        result = ""
        result += "id:\n" + str(self.id) + "\n\n"
        result += "text:\n" + self.text + "\n\n"
        result += "prev_sentence:\n" + str(self.prev_sentence) + "\n\n"
        result += "next_sentence:\n" + str(self.next_sentence) + "\n\n"
        result += "\n"
        return result


class NodeFactory:
    @classmethod
    def create_node(cls, title, headings, body_text, prev_node=None, next_node=None):
        return DocumentNode(title, headings, body_text, prev_node, next_node)


class SentenceFactory:
    @classmethod
    def create_sentence(cls, text, prev_sentence=None, next_sentence=None):
        sentence_id = generate_unique_id()
        return Sentence(sentence_id, text, prev_sentence, next_sentence)


if __name__ == '__main__':
    file_path = select_file()

    if file_path:
        document_xml_bytes = unzip_docx(file_path)
        document_xml = parse_document_xml(document_xml_bytes)
        remove_toc(document_xml)  # Add this line to remove the table of contents
        condense_blank_lines(document_xml)
        root = document_xml
        text_contents = extract_text_elements(root)
        document_nodes = {}
        prev_node_id = None
        current_title = ""
        current_headings = []
        for style, text_content, current_headings in text_contents:
            if style == "Title":
                current_title = text_content
            elif "Heading" in style:
                pass  # We are now processing headings in the extract_text_elements function
            else:
                node = NodeFactory.create_node(title=current_title, headings=r" \ ".join(current_headings),
                                               body_text=text_content, prev_node=prev_node_id)
                if prev_node_id is not None:
                    document_nodes[prev_node_id].next_node = node.id
                document_nodes[node.id] = node
                prev_node_id = node.id

        for node in document_nodes.values():
            print(node.to_string())
