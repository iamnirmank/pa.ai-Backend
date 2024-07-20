from Chatmate.Utility.parsing_utility import document_parser, link_parser


def load_documents():
    """Load documents from the database, extract text from files and links, and combine results."""
    from Chatmate.models import Documents
    documents = Documents.objects.all()

    print("documents", documents)

    file_paths = [doc.file.path for doc in documents if doc.file]
    print("file_paths", file_paths)
    links = [doc.link for doc in documents if doc.link]

    file_chunks = []
    if file_paths:
        for path in file_paths:
            file_chunks.extend(document_parser(path))
    
    link_chunks = link_parser(links) if links else []



    combined_chunks = link_chunks + file_chunks

    # Ensure combined_chunks only contains JSON-serializable data
    combined_chunks = [chunk_to_dict(chunk) for chunk in combined_chunks]
    
    return combined_chunks

def chunk_to_dict(chunk):
    """Convert chunk to a JSON-serializable dictionary if it's not already."""
    if isinstance(chunk, dict):
        return chunk
    elif hasattr(chunk, '__dict__'):
        return chunk.__dict__
    else:
        raise TypeError(f'Object of type {chunk.__class__.__name__} is not JSON serializable')

def update_combined_chunks():
    from Chatmate.models import CombinedChunk

    combined_chunks = load_documents()
    print("combined_chunks", combined_chunks)
    combined_chunk_instance, created = CombinedChunk.objects.get_or_create(id=1, defaults={'chunks': combined_chunks})
    if not created:
        combined_chunk_instance.chunks = combined_chunks
        combined_chunk_instance.save()
