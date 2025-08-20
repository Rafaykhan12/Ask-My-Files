# query_docs_chain.py
import os
from dotenv import load_dotenv
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough

# Load .env
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY not found in .env file")

DB_DIR = "vector_db"

############################## Document Query Chain #############################################

# Step 1: Prompt template (works for PDF + Word)
doc_template_str = """You are a helpful assistant.
Use the provided document content and file names to answer the user's question.
Be as detailed as possible, but do not make up any information not in the context.
If the answer is not in the context, say "I don't know."

For each part of your answer, include the file name it came from.

Context:
{context}
"""

doc_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=doc_template_str,
    )
)

doc_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)

messages = [doc_system_prompt, doc_human_prompt]
doc_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)

# Step 2: Model
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Step 3: Load DB
vector_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=OpenAIEmbeddings()
)
retriever = vector_db.as_retriever(k=6)

# Step 4: Custom wrapper to include file names in context
def retriever_with_sources(query):
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join(
        [f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in docs]
    )
    return context

# Step 5: Build chain
doc_chain = (
    {"context": retriever_with_sources, "question": RunnablePassthrough()}
    | doc_prompt_template
    | chat_model
    | StrOutputParser()
)

############################## Run Chain in Loop #############################################
print("💬 Document Q&A Chat (PDF + Word) - Press Ctrl+C to exit\n")

try:
    while True:
        query = input("❓ Enter your question: ").strip()
        if not query:
            print("⚠️ Please enter a question.")
            continue

        answer = doc_chain.invoke(query)

        print("\n💡 Answer:")
        print(answer)
        print("\n" + "-" * 80 + "\n")

except KeyboardInterrupt:
    print("\n👋 Exiting Document Q&A Chat. Goodbye!")

