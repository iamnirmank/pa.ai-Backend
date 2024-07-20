from sentence_transformers import SentenceTransformer
import faiss

class Document:
    def __init__(self, id_, text):
        self.id_ = id_
        self.text = text

class DocumentChunk:
    def __init__(self, id_, chunk_id, embedding=None, text=''):
        self.id_ = id_           
        self.chunk_id = chunk_id
        self.embedding = embedding
        self.text = text

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=100):
    """
    Splits text into chunks of approximately chunk_size words.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def process_documents(documents):
    """
    Processes each document into chunks and returns a list of DocumentChunk objects.
    """
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(DocumentChunk(id_=doc["id_"], chunk_id=i, text=chunk))
    return all_chunks

def compute_embeddings(chunks):
    """
    Computes embeddings for each chunk and assigns them to the chunk objects.
    """
    texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(texts)
    
    for chunk, embedding in zip(chunks, embeddings):
        chunk.embedding = embedding

    return embeddings

def create_index(embeddings):
    """
    Creates a FAISS index for the embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def retrieve_chunks(query, index, chunks, top_k=5):
    """
    Retrieves the most relevant chunks based on the query.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    
    # Retrieve the most relevant chunks based on indices
    relevant_chunks = [chunks[i] for i in indices[0]]
    return relevant_chunks, distances