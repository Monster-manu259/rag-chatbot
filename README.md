# RAG Chatbot
RAG Chatbot is an AI assistant that finds answers from your documents using fast vector search and advanced language models.
It delivers accurate, context-aware responses grounded in your own data.
Easy to set up, customize, and integrate into any application.

## Backend

The backend handles document processing, vector search, and response generation. Built with Python using FastAPI, it exposes API endpoints for the frontend and manages the workflow from query to response.

**Features:**
- API routing and query handling
- Document ingestion and embedding
- Vector database integration (Pinecone)
- Response generation using NLP models


## Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/Monster-manu259/rag-chatbot.git
   cd rag-chatbot
   ```

2. **Set up a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
## Configuration

- Create a .env file in the root directory of the project and add the following environment variables with your actual credentials:
```powershell
PINECONE_API_KEY="your-pinecone-api-key"
GOOGLE_API_KEY ="your-google-api-key"
```
## Usage

- **Start the chatbot server:**
  ```powershell
  uvicorn main:app --reload
  ```

## Frontend

The frontend is built with **Streamlit** and provides a user-friendly interface for interacting with the RAG chatbot. Users can upload PDF documents and ask questions directly from the browser. The frontend communicates with the backend to process documents and retrieve answers.

**Features:**
- Upload PDF files for processing
- Chat interface for Q/A
- Displays context-aware responses
- Connects to backend endpoints

**To run the frontend:**
```powershell
streamlit run app.py
```

See `app.py` for implementation details.



## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Frontend web application
- **FastAPI**: Backend API server
- **Pinecone**: Vector database for similarity search
- **Google Generative AI** (`google.generativeai`): Language model integration
- **LangChain** (`langchain_community`, `langchain_text_splitters`): Document loading and text splitting
- **Sentence Transformers** (`sentence_transformers`): Text embedding
- **PyMuPDF**: PDF document loader via LangChain
- **Pydantic**: Data validation and settings management
- **dotenv**: Environment variable management
- **tempfile**: Temporary file handling
- **os**: Operating system utilities


