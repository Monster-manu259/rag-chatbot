# src/utils/exceptions.py
class EmbeddingAPIError(Exception):
    """An error occurred while generating embeddings with the embedding model API."""
    pass

class PineconeAPIError(Exception):
    """An error occurred while interacting with the Pinecone vector database."""
    pass

class PineconeRetrievalError(Exception):
    """An error occurred while retrieving chunks from Pinecone."""
    pass

class DocumentProcessingError(Exception):
    """An error occurred while processing the document. Please check the file and try again."""
    pass

class RetrievingAPIError(Exception):
    """An error occurred while retrieving data from the API."""
    pass