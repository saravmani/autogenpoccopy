import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv()

# Set up ChromaDB client
chroma_client = chromadb.Client()

# Define an embedding function (OpenAI embeddings)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name="text-embedding-ada-002"
)

# Create a Chroma collection
collection = chroma_client.create_collection(
    name="my_rag_collection",
    embedding_function=openai_ef
)

# Add documents to ChromaDB
documents = [
    "AutoGen is a framework to build multi-agent applications.",
    "RAG stands for Retrieval-Augmented Generation, combining retrieval systems with LLMs.",
    "ChromaDB is a fast, simple vector store for building retrieval systems.",
]

ids = ["doc1", "doc2", "doc3"]

collection.add(
    documents=documents,
    ids=ids
)


import autogen
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

# Configure the LLM for AutoGen
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": "YOUR_OPENAI_API_KEY",
    }
]

llm_config = {"config_list": config_list}

# Define the Retriever function using ChromaDB
def rag_retrieve(query, top_k=2):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results['documents'][0]

# Create RetrieveUserProxyAgent
rag_agent = RetrieveUserProxyAgent(
    name="rag_agent",
    retrieve_config={
        "task": "qa",
        "docs_retriever": rag_retrieve,
        "max_retrievals": 3,
    },
    llm_config=llm_config,
     code_execution_config=False # <-- Add this line
)

# Create UserProxyAgent to communicate with RetrieveUserProxyAgent
user_agent = autogen.UserProxyAgent(
    name="user_agent",
    human_input_mode="ALWAYS",
    llm_config=llm_config,
    code_execution_config=False # <-- Add this line
)

user_agent.initiate_chat(
    rag_agent,
    message="What is AutoGen and how does ChromaDB help with RAG applications?"
)
