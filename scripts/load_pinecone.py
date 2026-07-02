import gzip
import json
import os
from pinecone import Pinecone, ServerlessSpec

# Use real key
pc = Pinecone(api_key="pcsk_5La4Zc_GcDwGPWQg1hqPVmmYTAYqiRw7oG31vD6UASDbVS12XLfLeazcxZd3jSAjqThxBs")

# Auto create index with correct dimension (512)
if "financial-10k" not in pc.list_indexes().names():
    pc.create_index(
        name="financial-10k",
        dimension=512,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print("Index 'financial-10k' created with 512 dimension.")

index = pc.Index("financial-10k")

with gzip.open("data/pinecone_vectors.jsonl.gz", "rt") as f:
    for line in f:
        vector = json.loads(line)
        if 'namespace' in vector:
            del vector['namespace']
        index.upsert(vectors=[vector])

print("Pinecone vectors loaded successfully!")
