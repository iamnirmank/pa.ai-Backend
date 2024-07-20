from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

def document_parser(file_path):
    """Parse the text of a document using LlamaParse."""
    try:
        # Set up parser
        parser = LlamaParse(result_type="markdown")

        # Define supported file extensions and their corresponding parsers
        supported_file_types = [
            '.pdf', '.602', '.abw', '.cgm', '.cwk', '.doc', '.docx', '.docm', 
            '.dot', '.dotm', '.hwp', '.key', '.lwp', '.mw', '.mcw', '.pages', 
            '.pbd', '.ppt', '.pptm', '.pptx', '.pot', '.potm', '.potx', '.rtf', 
            '.sda', '.sdd', '.sdp', '.sdw', '.sgl', '.sti', '.sxi', '.sxw', 
            '.stw', '.sxg', '.txt', '.uof', '.uop', '.uot', '.vor', '.wpd', 
            '.wps', '.xml', '.zabw', '.epub', '.jpg', '.jpeg', '.png', '.gif', 
            '.bmp', '.svg', '.tiff', '.webp', '.htm', '.html', '.xlsx', '.xls', 
            '.xlsm', '.xlsb', '.xlw', '.csv', '.dif', '.sylk', '.slk', '.prn', 
            '.numbers', '.et', '.ods', '.fods', '.uos1', '.uos2', '.dbf', 
            '.wk1', '.wk2', '.wk3', '.wk4', '.wks', '.123', '.wq1', '.wq2', 
            '.wb1', '.wb2', '.wb3', '.qpw', '.xlr', '.eth', '.tsv'
        ]

        # Check if the file type is supported
        file_extension_index = file_path.lower().rfind('.')
        if file_extension_index == -1:
            raise ValueError("No file extension found")

        extension = file_path[file_extension_index:]
        if extension not in supported_file_types:
            raise ValueError(f"Unsupported file type: {extension}")

        file_extractor = {extension: parser}
        documents = SimpleDirectoryReader(input_files=[file_path], file_extractor=file_extractor).load_data()
        return documents
    
    except Exception as e:
        print(f"Error parsing document: {str(e)}")
        return []

def link_parser(url):
    """Parse the text of a webpage using LlamaParse."""
    try:
        documents = SimpleWebPageReader(html_to_text=True).load_data(url)
        return documents
    except Exception as e:
        print(f"Error parsing link: {str(e)}")
        return []
