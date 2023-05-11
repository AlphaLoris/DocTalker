# docx_document_parser.py module

import zipfile
from lxml import etree
from docx import Document
from node import NodeFactory
import re


class DocxDocumentParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.document_xml_bytes = None
        self.document_title = None
        self.xml_tree = None
        self.doc_root = None
        self.nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        self.text_contents = None
        self.document_nodes = None

        # Extract text elements from the document
        with zipfile.ZipFile(self.file_path, 'r') as docx_zip:
            self.document_xml_bytes = docx_zip.read('word/document.xml')

        # Get the document title
        self.document_title = DocxDocumentParser.get_docx_title(self.file_path)

    def process_document(self):
        self.doc_root = self.parse()
        self.remove_toc()
        self.condense_blank_lines()
        self.text_contents = self.extract_text_elements()
        # Print the text contents to console
        print("Document text:\n" + str(self.text_contents))

        # Create a dictionary of nodes based on the text contents of the document
        self.document_nodes = {}
        prev_node_id = None
        current_title = self.document_title

        for style, text_content, current_headings, page_numbers in self.text_contents:
            if style == "Title":
                current_title = text_content
            elif "Heading" in style:
                pass  # We are now processing headings in the extract_text_elements function
            else:
                # Check if the text_content is not empty after stripping whitespace characters
                if text_content.strip():
                    node = NodeFactory.create_node(title=current_title, headings=r" \ ".join(current_headings),
                                                   body_text=text_content, prev_node=prev_node_id,
                                                   page_numbers=page_numbers)
                    if prev_node_id is not None:
                        self.document_nodes[prev_node_id].next_node = node.id
                    self.document_nodes[node.id] = node
                    prev_node_id = node.id

        return self.document_nodes

    # Attempt to get the title of a .docx file from its metadata.
    @staticmethod
    def get_docx_title(doc_file_path: str) -> str:
        doc = Document(doc_file_path)
        core_properties = doc.core_properties

        if core_properties.title:
            return core_properties.title

        for paragraph in doc.paragraphs:
            if paragraph.style.name == "Title" and paragraph.text.strip():
                return paragraph.text.strip()
        return ""

    def parse(self):
        self.doc_root = etree.fromstring(self.document_xml_bytes)
        self.xml_tree = self.doc_root  # Add this line to set the xml_tree
        return self.doc_root

    def remove_toc(self):
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
            toc_sdt.getparent().remove(toc_sdt)

            # Remove the header element, if it exists
            if header_element is not None:
                header_element.getparent().remove(header_element)

    def condense_blank_lines(self):
        namespaces = self.doc_root.nsmap
        paragraphs = self.doc_root.findall(".//w:p", namespaces)
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

    def extract_text_elements(self):
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

    def extract_page_numbers(self, paragraph):
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

