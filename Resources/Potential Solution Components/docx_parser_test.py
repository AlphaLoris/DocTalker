import tkinter as tk
from abc import abstractmethod
from pathlib import Path
from tkinter import filedialog
from typing import Dict, Optional, Union, List
from docx import Document
from gpt_index.readers.file.base_parser import ImageParserOutput

# TODO: Find out how this parses the text elements from the xml tree into such natural blocks of text.
# TODO: Combine this with text_block_extractor.py to get the best of both worlds.

"""
This script first extracts the xml tree from the .docx file and saves it to a file. It then parses the xml tree into
its text elements using the <w:t> tag, and composes them into natural blocks of text (better than 
text_block_extractor.py) and saves them to a .txt file.
"""


class BaseParser:
    """Base class for all parsers."""

    def __init__(self, parser_config: Optional[Dict] = None):
        """Init params."""
        self._parser_config = parser_config

    def init_parser(self) -> None:
        """Init parser and store it."""
        parser_config = self._init_parser()
        self._parser_config = parser_config

    @property
    def parser_config_set(self) -> bool:
        """Check if parser config is set."""
        return self._parser_config is not None

    @property
    def parser_config(self) -> Dict:
        """Check if parser config is set."""
        if self._parser_config is None:
            raise ValueError("Parser config not set.")
        return self._parser_config

    @abstractmethod
    def _init_parser(self) -> Dict:
        """Initialize the parser with the config."""

    @abstractmethod
    def parse_file(
        self, file: Path, errors: str = "ignore"
    ) -> Union[str, List[str], ImageParserOutput]:
        """Parse file."""


class DocxParser(BaseParser):
    """Docx parser."""

    def _init_parser(self) -> Dict:
        """Init parser."""
        return {}

    def parse_file(self, file: Path, errors: str = "ignore") -> str:
        """Parse file."""
        try:
            import docx2txt
        except ImportError:
            raise ImportError(
                "docx2txt is required to read Microsoft Word files: "
                "`pip install docx2txt`"
            )

        text = docx2txt.process(file)

        return text

    def extract_xml(self, file: Path) -> str:
        """Extract and return the XML content from the .docx file."""
        doc = Document(file)
        main_document_part = doc.part
        xml_content = main_document_part.blob

        return xml_content


def main():
    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()

    # Open file browser and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])

    if file_path:
        # Create a DocxParser instance
        parser = DocxParser()

        # Parse the .docx file and get the text content
        text = parser.parse_file(Path(file_path))

        # Extract the XML content from the .docx file
        xml_content = parser.extract_xml(Path(file_path))

        # Replace the .docx extension with -txt.txt and save the text content
        output_file_path = Path(file_path).with_stem(Path(file_path).stem + "docx_parser-txt").with_suffix(".txt")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(text)

        # Replace the .docx extension with -xml.xml and save the XML content
        output_xml_file_path = Path(file_path).with_stem(Path(file_path).stem + "docx_parser-xml").with_suffix(".xml")
        with open(output_xml_file_path, "wb") as output_xml_file:
            output_xml_file.write(xml_content)

        print(f"Text saved to: {output_file_path}")
        print(f"XML saved to: {output_xml_file_path}")


if __name__ == "__main__":
    main()
