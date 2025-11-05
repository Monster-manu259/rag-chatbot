from google.generativeai.generative_models import GenerativeModel
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from typing import List
from src.utils.exceptions import (
    EmbeddingAPIError,
    PineconeAPIError,
    RetrievingAPIError
)
from sentence_transformers import SentenceTransformer
from src.config.settings import settings
from src.config.pinecone_db import PineconeDB


class DocumentProcessor:
    def __init__(self):
        self.model = SentenceTransformer("intfloat/e5-base-v2")
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
            embedded_chunks = self.model.encode(texts, show_progress_bar=True)
            return embedded_chunks.tolist() if hasattr(embedded_chunks, 'tolist') else embedded_chunks
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
            query_embedding = self.model.encode([query])[0]
            if hasattr(query_embedding, 'tolist'):
                query_embedding = query_embedding.tolist()
            results = self.pinecone_db.query(vector=query_embedding, top_k=top_k, include_metadata=True)
            matches = results.get("matches", [])
            retrieved_chunks = [match["metadata"]["text"] for match in matches]
            return "\n".join(retrieved_chunks)
        except Exception as e:
            raise RetrievingAPIError(f"Error retrieving chunks: {str(e)}")

    def answer_query(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant chunks and generate answer using Gemini 2.5 Flash
        """
        retrieved_chunks = self.retrieving_chunks(query, top_k=top_k)
        context = "\n".join(retrieved_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        # Set API key using google.generativeai.client.configure
        try:
            from google.generativeai.client import configure
            configure(api_key=settings.GOOGLE_API_KEY)
            model = GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RetrievingAPIError(f"Error generating answer: {str(e)}")

