from Chatmate.Utility.text_extraction import link_parser, document_parser
from Chatmate.models import Documents

def load_documents():
    """Load documents from the database, extract text from files and links, and combine results."""
    documents = Documents.objects.all()

    # Separate documents into files and links
    file_paths = [doc.file.path for doc in documents if doc.file]
    links = [doc.link for doc in documents if doc.link]

    # Extract text from files and links
    file_chunks = []
    if file_paths:
        for path in file_paths:
            file_chunks.extend(document_parser(path))
    
    link_chunks = link_parser(links) if links else []

    # Combine file_chunks and link_chunks
    combined_chunks = link_chunks + file_chunks

    print("combined_chunks: ", combined_chunks)
    
    return combined_chunks
