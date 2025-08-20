# Ask-My-Files
AskMyFiles is an AI-powered document assistant that lets you chat with your files. Instead of manually searching through long PDFs, Word documents, or text files, simply upload your files and ask natural language questions. The system uses embeddings + LLMs to retrieve the most relevant information and provide accurate, context-aware answers.

# 📚 What This Project Does

## 📂 Document & Code Handling
- Loads PDF, Word (.docx), and TXT files (easy to extend to code files).  
- Splits documents (and code, if added) into chunks for efficient embedding.  

## 🧠 AI-Powered Understanding
- Creates embeddings using **OpenAI Embeddings** and stores them in **ChromaDB**.  
- Queries documents using **RAG (Retrieval-Augmented Generation)** with an LLM (ChatGPT).  
- Answers questions with context directly from your documents and includes source file names.  

## 👨‍💻 For Developers
- Quickly locate relevant sections in large codebases.  
- Find where to debug or trace an error.  
- Get explanations of unfamiliar code in plain language.  
- Acts like a smart search assistant for programming projects.  

## ⚖️ For Professionals (Lawyers, Doctors, Researchers, etc.)
- **Lawyers**: search case files, contracts, discovery, and precedent instantly.  
- **Doctors/Clinicians**: query patient reports, research papers, or medical guidelines.  
- **Researchers/Students**: summarize academic papers and pull key references.  
- **Business Teams**: extract insights from policy documents, compliance reports, or strategy files.  

# 🚀 Why Use AskMyFiles?
AskMyFiles saves time, reduces manual searching, and improves accuracy by letting you focus on decisions instead of digging through documents. Whether you’re coding, preparing legal arguments, analyzing research, or reviewing medical files, this tool acts like your personal AI knowledge assistant.


# 🚀 Installation
-1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/AskMyFiles.git  
cd AskMyFiles
``` 

-2️⃣ Create a virtual environment

```bash
python3 -m venv venv  
source venv/bin/activate   # Mac/Linux  
venv\Scripts\activate      # Windows
```

-3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

-4️⃣ Set up environment

```bash
cp .env.example .env  
#Edit .env and add your OpenAI API key
```
-🗂️ Prepare Documents

```bash
dfs/  
word_docs/  
txt_docs/ 
```

-🧱 Build Embeddings
-Run the embedding script to index all documents:

```bash
python create_embeddings.py
```

✅ This processes your documents, chunks them, and creates embeddings inside vector_db/.

-💬 Query with RAG (Chat Loop)

-Run the interactive Q&A:

```bash
python query_docs_chain.py
```

-You’ll get a prompt like:

```bash
❓ Enter your question:
```


-Ask anything about your documents.Answers include file references too.

Example:
```bash
❓ Enter your question: Do you have any research paper? If yes, then give me a summary of it

`💡 Answer:  
`Yes, I have a research paper titled "doc4.pdf." The paper provides an overview of the Internet of Things (IoT)...
```

