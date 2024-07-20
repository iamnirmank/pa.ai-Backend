# # user_data/milvus_utils.py

# import os
# from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# MILVUS_URI = os.environ.get("MILVUS_API_ENDPOINT")
# MILVUS_API_KEY = os.environ.get("MILVUS_API_KEY")

# connections.connect(
#     "default",
#     uri="https://in03-42fdb1f6a95c6dc.api.gcp-us-west1.zillizcloud.com",
#     api_key="e07d5785667b531cfba4c641401f7b729a427c813fee843a98833fd8a8a0b0ff8eb6ce3a675c6feeccb25937073cf24a482aebdb"
# )

# def create_collection(dim):
#     fields = [
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
#         FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
#     ]
#     schema = CollectionSchema(fields=fields, description="Document embeddings")
#     collection = Collection(name="document_collection", schema=schema)
#     return collection

# def insert_embeddings(ids, embeddings):
#     collection = Collection("document_collection")
#     collection.insert([ids, embeddings])
#     collection.load()

# def search_embedding(query_embedding, top_k=5):
#     collection = Collection("document_collection")
#     search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
#     results = collection.search(
#         data=[query_embedding],
#         anns_field="embedding",
#         param=search_params,
#         limit=top_k,
#         expr=None
#     )
#     return results

# def test_all_functionality(embeddings, ids, dim, query_embedding):
#     collection = create_collection(dim)
#     print("Collection created")
#     insert_embeddings(ids, embeddings)
#     print("Embeddings inserted")
#     results = search_embedding(query_embedding)
#     print("Search results:", results)
#     return results