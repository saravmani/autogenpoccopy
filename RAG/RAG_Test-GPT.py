
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Chroma DB
client = chromadb.PersistentClient(path="./chroma_db")

# Use OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name="text-embedding-ada-002"
)

# Create collection
collection = client.get_or_create_collection(name="docs", embedding_function=openai_ef)

# Load your document and add to collection
with open("FunctionalDocument.md", "r") as file:
    document_text = file.read()

# Split document into chunks (basic split by paragraph here, more sophisticated splitting recommended)
paragraphs = [para.strip() for para in document_text.split('\n') if para.strip()]

# Add paragraphs to Chroma DB
collection.add(
    documents=paragraphs,
    ids=[f"para_{i}" for i in range(len(paragraphs))]
)

# Step 3: Setup AutoGen RAG agent
import autogen

# Define retriever function using Chroma DB
def retrieve_context(query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return ' '.join(results['documents'][0])

# Define AutoGen agent with context retrieval
class RAGAgent(autogen.ConversableAgent):
    def generate_reply(self, messages, **kwargs):
        last_message = messages[-1]['content']
        context = retrieve_context(last_message)
        prompt = f"Answer the question based on the following context:\n{context}\n\nQuestion: {last_message}\nAnswer:"
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# Initialize AutoGen agent
rag_agent = RAGAgent(
    name="rag_agent",
    llm_config={
        "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.getenv('OPENAI_API_KEY')}],
    }
)

# User query example
user_query = "which api is for facebook"

# Agent generates response
response = rag_agent.generate_reply(messages=[{"role": "user", "content": user_query}])

print("Agent Response:", response)