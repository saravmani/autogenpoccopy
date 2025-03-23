
import os
from dotenv import load_dotenv
from autogen import  AssistantAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.retrieve_utils import TEXT_FORMATS # this the file format used to save the files in vector db
from chromadb.utils import embedding_functions

load_dotenv() 
 
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
  
llm_config_openApi = {
    "model": "gpt-3.5-turbo", 
    "api_key": OPENAI_API_KEY
    }


 

llm_config=llm_config_openApi


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-ada-002"
            )



assistant = AssistantAgent(
    name="assistant",
        system_message="Get the information from the context only and provide the answer. dont provide any extra",

   # system_message="You are a helpful AI assistant. You can help with simple calculations. Return 'TERMINATE' when the task is done.",
    llm_config=llm_config
)


ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=4,
    system_message="Assistant who has extra content retrieval power for solving difficult problems.",
    code_execution_config=False,

    retrieve_config={
        "task": "qa",
        "docs_path": "https://raw.githubusercontent.com/saravmani/mycloud/refs/heads/master/Rem/FunctionalDocument.md",        
        # "docs_path": "./knowledge-base",
        "embedding_function": openai_ef,
        "get_or_create": True,
        "chunk_token_size": 1000,

         "top_k": 2 , # returns top 3 closest chunks instead of default (usually 5)

     "chunk_overlap": 500,  # ensure continuity between chunks
        
        "embedding_model": "text-embedding-ada-002",
        "model":  'gpt-3.5-turbo', 
        "vector_db": "chroma",
        "overwrite": True,  # set to True if you want to overwrite an existing collection
      
        }
)




assistant.reset()
 

chat_result = ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem="what is the exact  Data Structures?")

 
chat_history = chat_result.chat_history

if chat_history and len(chat_history) > 0:
    latest_message = chat_history[0]

    # Print the retrieved context
    if "context" in latest_message:
        print("Retrieved Context:")
        print(latest_message["context"])
    else:
        print("No Context Retrieved.")

    # Print the assistant's response
    print("\nAssistant's Response:**********************")
    print(latest_message["content"])