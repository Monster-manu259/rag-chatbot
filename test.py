from src.utils.document_processing import DocumentProcessor
processor = DocumentProcessor()

query = "what are the APMC online services?"
answer = processor.retrieving_chunks(query)
print("result:", answer)
