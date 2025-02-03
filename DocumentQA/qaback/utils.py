# import os
# import shutil
# from langchain_community.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.schema.output_parser import StrOutputParser
# from langchain.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# load_dotenv()

# PERSIST_DIRECTORY = "chroma_db"

# # Initialize embeddings and LLM
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

# prompt = ChatPromptTemplate.from_template(
#     """You are an assistant for question-answering tasks.
# Use the following pieces of retrieved context to answer the question.
# If you don't know the answer, just say that you don't know.
# Give the complete answer in correct way and in points if it required.
# Question: {question}
# Context: {context}
# Answer:
# """
# )

# vector_db = None  # Global vector database

# def process_pdf(pdf_path):
#     global vector_db
#     os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

#     loader = PyPDFLoader(pdf_path, extract_images=True)
#     pages = loader.load()
#     docs = text_splitter.split_documents(pages)

#     # Clean previous DB
#     if os.path.exists(PERSIST_DIRECTORY):
#         shutil.rmtree(PERSIST_DIRECTORY)

#     vector_db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
#     vector_db.persist()

# def get_answer(question):
#     global vector_db
#     if not vector_db:
#         return "No PDF has been uploaded yet."

#     retriever = vector_db.as_retriever()
#     output_parser = StrOutputParser()

#     rag_chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | prompt
#         | llm
#         | output_parser
#     )

#     return rag_chain.invoke(question)

# import os
# import shutil
# from langchain_community.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.schema.output_parser import StrOutputParser
# from langchain.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# from langchain.vectorstores import Weaviate
# import locale
# import asyncio
# from cachetools import TTLCache
# import nest_asyncio


# load_dotenv()
# # Update paths to use absolute paths
# PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
# MEDIA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
# # Ensure media directory exists
# os.makedirs(MEDIA_DIRECTORY, exist_ok=True)

# # Initialize embeddings and LLM
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

# prompt = ChatPromptTemplate.from_template(
#     """You are an assistant for question-answering tasks.
# Use the following pieces of retrieved context to answer the question.
# If you don't know the answer, just say that you don't know.
# Provide answers in a well-structured manner, using bullet points if necessary.

# Question: {question}
# Context: {context}
# Answer:
# """
# )

# vector_db = None  # Global vector database



# def process_pdf(pdf_path):
#     """Process the PDF, delete old ChromaDB, and create a new vector database."""
#     global vector_db
#     vector_db = None  # This forces reinitialization

  

#     # Delete previous ChromaDB
#     if os.path.exists(PERSIST_DIRECTORY):
#         shutil.rmtree(PERSIST_DIRECTORY)
    
#     os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

#     # Load and split PDF
#     loader = PyPDFLoader(pdf_path, extract_images=True)
#     pages = loader.load()
#     docs = text_splitter.split_documents(pages)

#     # Create new vector store
#     vector_db = Chroma.from_documents(
#         documents=docs,
#         embedding=embeddings,
#         persist_directory=PERSIST_DIRECTORY
#     )
#     vector_db.persist()

# def get_answer(question):
#     """Retrieve answer from ChromaDB using the question."""
#     global vector_db
#     if not vector_db:
#         return "No PDF has been uploaded yet."

#     retriever = vector_db.as_retriever()
#     output_parser = StrOutputParser()

#     rag_chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | prompt
#         | llm
#         | output_parser
#     )

#     # Convert response into a point-wise format
#     answer = rag_chain.invoke(question)
#     formatted_answer = "\n".join([f"- {line.strip()}" for line in answer.split(". ") if line])

#     return formatted_answer
import os
import shutil
from langchain_community.vectorstores import FAISS  # Changed import
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Update paths
PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faiss_db")
MEDIA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(MEDIA_DIRECTORY, exist_ok=True)

# Initialize components
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

prompt = ChatPromptTemplate.from_template(    """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Give the complete answer in correct way and in points if it required.
Question: {question}
Context: {context}
Answer:
""")

vector_db = None

def process_pdf(pdf_path):
    """Process PDF using FAISS vector store"""
    global vector_db
    vector_db = None

    # Clear previous FAISS index
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
    
    # Create fresh directory
    os.makedirs(PERSIST_DIRECTORY, mode=0o755, exist_ok=True)

    # Load and process PDF
    loader = PyPDFLoader(pdf_path, extract_images=True)
    pages = loader.load()
    docs = text_splitter.split_documents(pages)

    # Create and save FAISS index
    vector_db = FAISS.from_documents(
        documents=docs,
        embedding=embeddings
    )
    vector_db.save_local(PERSIST_DIRECTORY)

def get_answer(question):
    """Retrieve answer from FAISS index"""
    global vector_db
    if not vector_db:
        return "No PDF has been uploaded yet."

    # Load FAISS index
    vector_db = FAISS.load_local(
        folder_path=PERSIST_DIRECTORY,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vector_db.as_retriever()
    
    # Rest of your existing RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)
    return "\n".join([f"- {line.strip()}" for line in answer.split(". ") if line])
