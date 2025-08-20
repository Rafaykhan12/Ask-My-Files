import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY not found in .env file")

# Directories
PDF_DIR = "pdfs"
WORD_DIR = "word_docs"
TXT_DIR = "txt_docs"
DB_DIR = "vector_db"

# Step 1: Load documents from all formats
documents = []

# PDFs
for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        path = os.path.join(PDF_DIR, file)
        loader = PyPDFLoader(path)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file
        documents.extend(docs)

# Word Docs
for file in os.listdir(WORD_DIR):
    if file.endswith(".docx"):
        path = os.path.join(WORD_DIR, file)
        loader = Docx2txtLoader(path)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file
        documents.extend(docs)

# TXT files
for file in os.listdir(TXT_DIR):
    if file.endswith(".txt"):
        path = os.path.join(TXT_DIR, file)
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file
        documents.extend(docs)

# Step 2: Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Step 3: Create embeddings
embedding_function = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    chunks,
    embedding_function,
    persist_directory=DB_DIR
)

vectorstore.persist()
print(f"✅ Embeddings created for PDFs, Word docs, and TXT files in '{DB_DIR}'")
