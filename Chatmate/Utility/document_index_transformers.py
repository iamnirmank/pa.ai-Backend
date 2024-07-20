# import os
# from Chatmate.Utility.text_extraction import document_parser, extract_text, link_parser
# from Chatmate.models import Documents
# from pymilvus import MilvusClient, DataType
# from sentence_transformers import SentenceTransformer

# # Initialize the embedding model
# def init_embeddings():
#     """Initialize the Milvus collection."""
#     embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
#     return embedding_model

# # Zilliz Cloud cluster details
# def init_milvus():
#     """Initialize the Milvus client and create a collection."""
#     # Zilliz Cloud cluster details
#     CLUSTER_ENDPOINT = os.environ.get('MILVUS_API_ENDPOINT')
#     TOKEN = os.environ.get('MILVUS_API_KEY')

#     # Set up a Milvus client
#     client = MilvusClient(
#         uri=CLUSTER_ENDPOINT,
#         token=TOKEN 
#     )
#     # Create a collection schema
#     schema = MilvusClient.create_schema(
#         auto_id=True,
#         enable_dynamic_field=True,
#     )

#     collection_name = 'document_embeddings'

#     # Check if the collection exists
#     if not client.has_collection(collection_name):
#         # Add fields to schema
#         schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=384)
#         schema.add_field(field_name="doc_id", datatype=DataType.INT64, is_primary=True)

#         # Create the collection
#         client.create_collection(
#             collection_name="document_embeddings",
#             schema=schema
#         )

#     return client

# def load_documents():
#     """Load documents from the database and extract text."""
#     documents = Documents.objects.all()
#     chunks = []
#     for doc in documents:
#         file_path = doc.file.path
#         text = extract_text(file_path)
#         chunks.append(text)
#     return chunks

# def index_documents(client, embedding_model):
#     """Index the documents into Milvus."""
#     chunks = load_documents()
#     embeddings = embedding_model.encode(chunks)

#     # Prepare data for insertion
#     data = [
#         {
#             "embedding": emb.tolist()
#         } for emb in embeddings
#     ]

#     # Insert data into Milvus
#     client.insert(
#         collection_name="document_embeddings",
#         data=data
#     )

# def drop_collection(client):
#     """Drop the Milvus collection."""
#     collection_name = "document_embeddings"
#     if client.has_collection(collection_name):
#         client.drop_collection(collection_name)
