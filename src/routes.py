from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from src.utils.document_processing import DocumentProcessor

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    processor = DocumentProcessor()
    for file in files:
        path = f"temp_{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        docs = processor.page_content(path)
        chunks = processor.chunks_conversion(docs)
        embeds = processor.embedding(chunks)
        processor.add_embeddings_to_pinecone(embeds, chunks)
    return {"message": "All files processed and embeddings added to Pinecone.",
            "status": "success",
            "ValueError": None,
            "status_code": 200 }

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    processor = DocumentProcessor()
    results = processor.answer_query(request.query, top_k=request.top_k)
    return {"results": results}
