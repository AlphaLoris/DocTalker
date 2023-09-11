"""
docx_document_parser.py Module

This module provides a DocxDocumentParser class for parsing and processing .docx files. The class extracts text
elements, removes table of contents (TOC), condenses blank lines, and creates a dictionary of document nodes based on
the text contents.

Usage
    1. Create an instance of the DocxDocumentParser class, providing the file path as input.
    2. Use the process_document method to parse and process the document.
    3. Access the extracted text contents and document nodes for further processing.

Dependencies:
    - zipfile
    - etree from lxml
    - Document from docx
    - NodeFactory from node
    - re

Notes:
    - The DocxDocumentParser class handles the parsing and processing of .docx files.
    - The class extracts text elements, removes TOC, condenses blank lines, and creates document nodes.
    - The document title is extracted from the metadata or the document body.
    - The process_document method returns a dictionary of document nodes.
    - The extract_text_elements method extracts text contents and handles headings.
    - The remove_toc method removes the TOC element and the header element, if present.
    - The condense_blank_lines method removes excessive blank lines and adjusts spacing.
    - The extract_page_numbers method extracts page numbers from page breaks.
"""

# docx_document_parser.py

import zipfile
from lxml import etree
from lxml.etree import ElementBase
from docx import Document
from node import DocumentNode, NodeFactory
from typing import Dict, List, Tuple
import re
import logging
from utils.log_config import setup_colored_logging

# Setup Logging
setup_colored_logging()
logger = logging.getLogger(__name__)


class DocxDocumentParser:
    """
    This class provides a parser for .docx documents. It is capable of extracting text elements,
    removing TOCs, condensing blank lines, and creating document nodes from the extracted text.
    """
    def __init__(self, file_path: str):
        """
        Initializes the parser with the given file path.

        :param file_path: Path to the .docx document to be parsed.
        :type file_path: str
        """
        self.file_path = file_path
        self.document_xml_bytes = None
        self.document_title = None
        self.xml_tree = None
        self.doc_root = None
        self.nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        self.text_contents = None
        self.document_nodes = None
        logger.debug(f"Initializing DocxDocumentParser for file: {self.file_path}")

        # Extract text elements from the document
        with zipfile.ZipFile(self.file_path, 'r') as docx_zip:
            self.document_xml_bytes = docx_zip.read('word/document.xml')

        # Get the document title
        self.document_title = DocxDocumentParser.get_docx_title(self.file_path)

    def process_document(self) -> Dict[str, DocumentNode]:
        """
        Parses and processes the document. Returns a dictionary of document nodes.

        :return: A dictionary of document nodes. The keys are the node IDs and the values are the nodes.
        :rtype: Dict[str, Node]
        """
        self.doc_root = self.parse()
        self.remove_toc()
        self.condense_blank_lines()
        self.text_contents = self.extract_text_elements()

        logger.info(f"Processing document at path: {self.file_path}")

        # Print the entire text content of the document to console
        # logger.info("Document text:\n" + str(self.text_contents))

        # Print the first 25 words of the document to console
        logger.info("Document text: " + ' '.join(str(self.text_contents).split()[:25]) + (
            "..." if len(str(self.text_contents).split()) > 25 else ""))

        # Create a dictionary of nodes based on the text contents of the document
        self.document_nodes = {}
        prev_node_id = None
        current_title = self.document_title

        for style, text_content, current_headings, page_numbers in self.text_contents:
            if style == "Title":
                current_title = text_content
                print("Getting title from document body: " + current_title)
            elif "Heading" in style:
                pass  # We are now processing headings in the extract_text_elements function
            else:
                # Check if the text_content is not empty after stripping whitespace characters
                if text_content.strip():
                    print("Using process_document to create node for: " + text_content)
                    node = NodeFactory.create_node(title=current_title, headings=r" \ ".join(current_headings),
                                                   body_text=text_content, prev_node=prev_node_id)
                    if prev_node_id is not None:
                        self.document_nodes[prev_node_id].next_node = node.id
                    self.document_nodes[node.id] = node
                    prev_node_id = node.id

        print("Returning document nodes")
        return self.document_nodes

    # Attempt to get the title of a .docx file from its metadata.
    @staticmethod
    def get_docx_title(doc_file_path: str) -> str:
        """
        Attempts to get the title of a .docx file from its metadata.

        :param doc_file_path: Path to the .docx document.
        :type doc_file_path: str
        :return: The title of the document, or an empty string if no title could be found.
        :rtype: str
        """
        doc = Document(doc_file_path)
        core_properties = doc.core_properties

        logger.debug(f"Fetching title from metadata of document at path: {doc_file_path}")
        if core_properties.title:
            return core_properties.title

        for paragraph in doc.paragraphs:
            if paragraph.style.name == "Title" and paragraph.text.strip():
                return paragraph.text.strip()
        return ""

    def parse(self) -> ElementBase:
        """
        Parses the document and returns its XML root element.

        :return: The root element of the XML tree representing the document.
        :rtype: etree._Element
        """
        logger.debug("Parsing the document to extract XML root element.")
        self.doc_root = etree.fromstring(self.document_xml_bytes)
        self.xml_tree = self.doc_root
        return self.doc_root

    def remove_toc(self) -> None:
        """
        Removes the Table of Contents (TOC) and its header if it exists from the document.
        """
        logger.debug("Attempting to remove Table of Contents (TOC) from document.")
        xpath_toc = "//w:sdt/w:sdtPr/w:docPartObj/w:docPartGallery[@w:val='Table of Contents']"

        # Find the TOC element
        toc_elements = self.xml_tree.xpath(xpath_toc, namespaces=self.nsmap)

        # Find the header element preceding the TOC, if it exists
        header_element = None
        if toc_elements:
            toc_element = toc_elements[0]
            toc_sdt = toc_element.getparent().getparent().getparent()
            prev_element = toc_sdt.getprevious()
            if prev_element is not None and prev_element.xpath("local-name()") == "p" and \
                    prev_element.find("w:pPr/w:pStyle[@w:val='Heading1']", namespaces=self.nsmap) is not None:
                header_element = prev_element

            # Remove the TOC
            logger.info("Removing TOC")
            toc_sdt.getparent().remove(toc_sdt)

            # Remove the header element, if it exists
            if header_element is not None:
                header_element.getparent().remove(header_element)

    def condense_blank_lines(self) -> None:
        """
        Removes consecutive blank lines from the document and adjusts line spacing.
        """
        namespaces = self.doc_root.nsmap
        paragraphs = self.doc_root.findall(".//w:p", namespaces)
        remove_elements = []
        last_was_blank = False

        logger.debug("Condensing consecutive blank lines in the document.")
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

    def extract_text_elements(self) -> List[Tuple[str, str, List[str], List[int]]]:
        """
        Extracts text elements from the document and handles headings.

        :return: A list of tuples, where each tuple represents a text element and its properties.
        :rtype: List[Tuple[str, str, List[str], List[int]]]
        """
        logger.debug("Extracting text elements from the document.")
        paragraphs = self.doc_root.findall('.//w:p', self.doc_root.nsmap)
        doc_text_contents = []
        doc_current_headings = []

        for paragraph in paragraphs:
            paragraph_style = paragraph.find('.//w:pPr/w:pStyle', self.doc_root.nsmap)
            doc_style = paragraph_style.get(
                f'{{{self.doc_root.nsmap["w"]}}}val') if paragraph_style is not None else 'Body'
            runs = paragraph.findall('.//w:r', self.doc_root.nsmap)
            current_text = ""

            for run in runs:
                text_elements = run.findall('.//w:t', self.doc_root.nsmap)
                line_breaks = run.findall('.//w:br', self.doc_root.nsmap)

                for text_element in text_elements:
                    doc_text_content = text_element.text
                    current_text += doc_text_content

                if line_breaks:
                    current_text += "\n"

            page_numbers = self.extract_page_numbers(paragraph)

            if "Heading" in doc_style:
                heading_level = int(doc_style[-1])
                if len(doc_current_headings) >= heading_level:
                    doc_current_headings = doc_current_headings[:heading_level - 1]
                doc_current_headings.append(current_text.strip())
                doc_text_contents.append((doc_style, "", doc_current_headings.copy(), page_numbers))
            else:
                if doc_text_contents and doc_text_contents[-1][0] == "Body":
                    doc_text_contents[-1] = ("Body", doc_text_contents[-1][1] + "\n" + current_text.strip(),
                                             doc_current_headings.copy(), page_numbers)
                else:
                    doc_text_contents.append(
                        ("Body", current_text.strip(), doc_current_headings.copy(), page_numbers))

        return doc_text_contents

    def extract_page_numbers(self, paragraph: ElementBase) -> List[int]:
        """
        Extracts page numbers from the given paragraph element.

        :param paragraph: An XML element representing a paragraph in the document.
        :type paragraph: etree._Element
        :return: A list of page numbers extracted from the paragraph.
        :rtype: List[int]
        """
        logger.debug("Extracting page numbers from a paragraph in the document.")
        page_breaks = paragraph.findall(".//w:br[@w:type='page']", namespaces=self.nsmap)
        page_numbers = []

        for page_break in page_breaks:
            pb_parent = page_break.getparent()
            pb_index = pb_parent.index(page_break)
            if pb_index > 0:
                prev_sibling = pb_parent[pb_index - 1]
                if prev_sibling.tag.endswith("instrText") and "PAGE" in prev_sibling.text:
                    page_number_match = re.search(r'\d+', prev_sibling.text)
                    if page_number_match:
                        page_number = int(page_number_match.group())
                        page_numbers.append(page_number)
        return page_numbers
