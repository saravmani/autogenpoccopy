import os
from dotenv import load_dotenv
load_dotenv() 
 
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  
  



from autogen import AssistantAgent
from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB
chroma = ChromaVectorDB(path="./chroma_db_haystack")
 
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent


config_list = [
  {
      "model": "gpt-3.5-turbo", 
    "api_key": OPENAI_API_KEY,
  }
]

SYSTEM_PROMPT = """
You are a knowledgeable librarian that answers questions from your supervisor.
Constraints:
- Be accurate and precise. Dont give unknown answer.
- Answer briefly, in few words.
- Reflect on your answer, and if you think you are hallucinating, repeat this answer.
"""
system_message = {'role': 'system',  'content': SYSTEM_PROMPT}

agent = AssistantAgent(
  name="techno_business_agent",
  system_message=SYSTEM_PROMPT,
  human_input_mode="NEVER",
  llm_config={
    "config_list": config_list,
    "timeout": 180,
    "temperature": 0.2},
)

user = RetrieveUserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "qa",
        "docs_path": "https://raw.githubusercontent.com/saravmani/mycloud/refs/heads/master/Rem/FunctionalDocument.md",
        "vector_db": chroma,
        "embedding_model": "text-embedding-ada-002",
        "get_or_create": True,
         "chunk_token_size": 1000,
    },

 
    code_execution_config=False,
)
msg = "anything relatd to PARIS mentioned this document?"
user.initiate_chat(agent, message=user.message_generator, problem=msg)