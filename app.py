import streamlit as st
from src.utils.document_processing import process_and_store_pdf, retrieving_chunksr

st.set_page_config(page_title="Document Q/A Chatbot", layout="wide")

st.title("Document Q/A Chatbot")

menu = ["Upload Data", "Q/A"]
choice = st.sidebar.radio("Select Option", menu)

if choice == "Upload Data":
    st.header("Upload PDF Files")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                process_and_store_pdf(file)
        st.success("All files processed and stored!")

elif choice == "Q/A":
    st.header("Ask a Question")
    user_query = st.text_input("Enter your question:")
    if st.button("Get Answer") and user_query:
        with st.spinner("Retrieving answer..."):
            answer = retrieving_chunksr(user_query)
        st.write("**Answer:**", answer)
