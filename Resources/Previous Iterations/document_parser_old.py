# document_parser_old.py module

from lxml import etree


class DocumentParser:
    def __init__(self, document_xml_bytes, document_title):
        self.document_xml_bytes = document_xml_bytes
        self.document_title = document_title
        self.xml_tree = None
        self.doc_root = None
        self.nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # Attempt to get the title of a .docx file from its metadata.
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

    def remove_toc(self, xml_tree):
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

            if "Heading" in doc_style:
                heading_level = int(doc_style[-1])
                if len(doc_current_headings) >= heading_level:
                    doc_current_headings = doc_current_headings[:heading_level - 1]
                doc_current_headings.append(current_text.strip())
                doc_text_contents.append((doc_style, "", doc_current_headings.copy()))
            else:
                if doc_text_contents and doc_text_contents[-1][0] == "Body":
                    doc_text_contents[-1] = ("Body", doc_text_contents[-1][1] + "\n" + current_text.strip(),
                                             doc_current_headings.copy())
                else:
                    doc_text_contents.append(("Body", current_text.strip(), doc_current_headings.copy()))

        return doc_text_contents
