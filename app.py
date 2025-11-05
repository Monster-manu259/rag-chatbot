import streamlit as st
from src.utils.document_processing import DocumentProcessor

st.set_page_config(page_title="Document Q/A Chatbot", layout="wide")

st.title("Document Q/A Chatbot")

menu = ["Upload Data", "Q/A"]
choice = st.sidebar.radio("Select Option", menu)

# Initialize processor outside the conditional blocks
processor = DocumentProcessor()

if choice == "Upload Data":
    st.header("Upload PDF Files")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        import tempfile
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                processor.page_content(tmp_file_path)
        st.success("All files processed and stored!")

elif choice == "Q/A":
    st.header("Ask a Question")
    user_query = st.text_input("Enter your question:")
    if st.button("Get Answer") and user_query:
        with st.spinner("Retrieving answer..."):
            answer = processor.answer_query(user_query)
        st.write("**Answer:**", answer)
