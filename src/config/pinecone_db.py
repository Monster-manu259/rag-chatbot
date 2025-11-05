from pinecone import Pinecone, ServerlessSpec
from .settings import settings

class PineconeDB:
    def __init__(self, index_name="chatbot", dimension=768, metric="cosine", cloud="aws", region="us-east-1"):
        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set in environment variables.")
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = index_name
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud=cloud, region=region)
            )
        self.index = self.pc.Index(self.index_name)

    def upsert(self, vectors):
        return self.index.upsert(vectors=vectors)

    def query(self, vector, top_k=5, include_metadata=True):
        return self.index.query(vector=vector, top_k=top_k, include_metadata=include_metadata)
