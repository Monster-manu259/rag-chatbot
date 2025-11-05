from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from src.utils.exceptions import (
    EmbeddingAPIError,
    PineconeAPIError,
    RetrievingAPIError
)
from google.generativeai.client import configure
from google.generativeai.embedding import embed_content
from src.config.settings import settings
from src.config.pinecone_db import PineconeDB

class DocumentProcessor:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        configure(api_key=settings.GOOGLE_API_KEY)
        self.pinecone_db = PineconeDB()

    def page_content(self, pdf_path: str) -> List:
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()
        return docs

    def chunks_conversion(self, docs) -> list[str]:
        if isinstance(docs, list):
            combined_content = "\n".join([page.page_content for page in docs])
        else:
            combined_content = str(docs)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_text(combined_content)
        return texts

    def embedding(self, texts) -> List[List[float]]:
        try:
            response = embed_content(model="intfloat/e5-base-v2", content=texts)
            embedded_chunks = response["embedding"]
            return embedded_chunks
        except Exception as e:
            raise EmbeddingAPIError(f"Embedding API error: {e}")

    def add_embeddings_to_pinecone(self, doc_embeddings, document_chunks):
        try:
            vectors = [
                (
                    f"chunk-{i}",
                    doc_embeddings[i],
                    {"text": document_chunks[i]}
                )
                for i in range(len(doc_embeddings))
            ]
            self.pinecone_db.upsert(vectors)
            print(f"Successfully inserted {len(vectors)} document chunks into Pinecone index '{self.pinecone_db.index_name}'")
        except Exception as e:
            raise PineconeAPIError(f"Pinecone error: {e}")

    def retrieving_chunks(self, query: str, top_k: int = 5) -> str:
        try:
            response = embed_content(model="models/embedding-001", content=[query])
            query_embedding = response["embedding"][0]
            results = self.pinecone_db.query(vector=query_embedding, top_k=top_k, include_metadata=True)
            matches = results.get("matches", [])
            retrieved_chunks = [match["metadata"]["text"] for match in matches]
            return "\n".join(retrieved_chunks)
        except Exception as e:
            raise RetrievingAPIError(f"Error retrieving chunks: {str(e)}")

