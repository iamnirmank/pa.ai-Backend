from Chatmate.Utility.parsing_utility import document_parser, link_parser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents():
    """Load documents from the database, extract text from files and links, and combine results."""
    try:
        from Chatmate.models import Documents
        documents = Documents.objects.all()

        logger.info(f"Loaded {len(documents)} documents from the database.")

        file_paths = [doc.file.path for doc in documents if doc.file]
        logger.info(f"Extracted {len(file_paths)} file paths from documents.")
        links = [doc.link for doc in documents if doc.link]

        file_chunks = []
        for path in file_paths:
            try:
                file_chunks.extend(document_parser(path))
            except Exception as e:
                logger.error(f"Error parsing document at {path}: {str(e)}")

        link_chunks = []
        if links:
            try:
                link_chunks = link_parser(links)
            except Exception as e:
                logger.error(f"Error parsing links: {str(e)}")

        combined_chunks = link_chunks + file_chunks

        # Ensure combined_chunks only contains JSON-serializable data
        combined_chunks = [chunk_to_dict(chunk) for chunk in combined_chunks]

        return combined_chunks

    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        return []

def chunk_to_dict(chunk):
    """Convert chunk to a JSON-serializable dictionary if it's not already."""
    try:
        if isinstance(chunk, dict):
            return chunk
        elif hasattr(chunk, '__dict__'):
            return chunk.__dict__
        else:
            raise TypeError(f'Object of type {chunk.__class__.__name__} is not JSON serializable')
    except Exception as e:
        logger.error(f"Error converting chunk to dict: {str(e)}")
        return {}

def update_combined_chunks():
    from Chatmate.models import CombinedChunk
    try:
        combined_chunks = load_documents()
        logger.info(f"Combined chunks: {combined_chunks}")

        combined_chunk_instance, created = CombinedChunk.objects.get_or_create(id=1, defaults={'chunks': combined_chunks})
        if not created:
            combined_chunk_instance.chunks = combined_chunks
            combined_chunk_instance.save()
            logger.info("Combined chunks updated successfully.")
        else:
            logger.info("Combined chunks created successfully.")
    except Exception as e:
        logger.error(f"Error updating combined chunks: {str(e)}")

