import os
import numpy as np
# from Chatmate.Utility.huggingface_response import generate_response_with_llama
# from Chatmate.Utility.together_ai_response import generate_response_with_llama
from Chatmate.Utility.groq_response import generate_response_with_llama
from Chatmate.Utility.processing_documents import load_documents
from Chatmate.Utility.indexing_documents import compute_embeddings, create_index, process_documents, retrieve_chunks
import faiss

def process_query(query):
    """Process a user query by retrieving relevant documents and generating a response."""
    context = context_extraction(query)
    additional_note = "Give the detailed answer in a very detailed manner with the natural tone of the language."
    combined_input = f"Context: {context}\n\nQuestion: {query}\n\nAdditional Note: {additional_note}\n\nAnswer:"
    response = generate_response_with_llama(combined_input)
    # response = "This is a response"
    return response

def context_extraction(query):
    """Index the documents into Milvus using LlamaIndex."""
    chunk = load_documents()

    chunks = process_documents(chunk)
    embeddings = compute_embeddings(chunks)
    index = create_index(np.array(embeddings))
    faiss.write_index(index, "chunks_index.faiss")

    index = faiss.read_index("chunks_index.faiss")
    relavant_chunks, distances = retrieve_chunks(query, index, chunks)

    os.remove("chunks_index.faiss")

    context = "\n".join([chunk.text for chunk in relavant_chunks])

    return context