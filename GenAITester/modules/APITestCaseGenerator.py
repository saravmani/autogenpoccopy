## Test case generation without BDD

import os
from dotenv import load_dotenv
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm_config_openApi = {
    "model": "gpt-4o",
    "api_key": OPENAI_API_KEY
}

llm_config = llm_config_openApi

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-ada-002"
)


class APITestCaseGenerator:
    def __init__(self,baseApiUrl,componentName):
        self.assistant = AssistantAgent(
            name="assistant",
            system_message="You are expert in writting API test cases in pytest using python with request package,  based on the scenarios and context." 
            "Also you follow the proper python syntext and return the exact python code. "
            "The test cases should be Autonomous and independent. "
            "If required have presetup Ex: For duplicate/existing check condition as part of setup create first then create second time"
            
            "BASE_URL = "+ baseApiUrl + 
            "Sample code in pytest: "
            """
                import pytest
                import requests

                BASE_URL = "http://localhost:8080"  # Example API
                def test_get_posts():
                    response = requests.get(f"{BASE_URL}/posts")
                    assert response.status_code == 200
                    posts = response.json()
                    assert isinstance(posts, list)

            -------------------------------------
            
            Return TERMINATE when you are done
            """
            
            
            ,
            llm_config=llm_config 
        )

        self.ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            system_message="Assistant who has extra content retrieval power for solving difficult problems.",
            code_execution_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],

            retrieve_config={
                "task": "qa",
                # "docs_path": "https://raw.githubusercontent.com/saravmani/mycloud/refs/heads/master/Rem/FunctionalDocument.md",        
                "docs_path": "./documents",
                "embedding_function": openai_ef,
                "get_or_create": True,
                "chunk_token_size": 2000,
                "top_k": 3 , # returns top 3 closest chunks instead of default (usually 5)
                "chunk_overlap": 500,  # ensure continuity between chunks                
                "embedding_model": "text-embedding-ada-002",
                "model":  'gpt-4o', 
                "vector_db": "chroma",
                "overwrite": True,  # set to True if you want to overwrite an existing collection
            
                }
        )

    def read_file_content(self, file_name):
        file_path = os.path.join(os.getenv('BDDFILESPATH'), file_name)
        with open(file_path, 'r',encoding='utf-8') as file:
            content = file.read()
        return content
    
    def generate_pytest_testcases(self, test_data_dictionary):                
        for filename in os.listdir(os.getenv('BDDFILESPATH')):
                    if filename.endswith(".feature"):
                        content = self.read_file_content(filename)
                        api_url = filename.replace("_","/").split(".")[0]
                        task = "Generate pytest test cases for the given BDD test case Scenarios:  " + content+  "Api URL :  "+api_url                 
                                                
                        
                        self.generate_pytest_testcases_for_features(task)
                        

    def generate_pytest_testcases_for_features(self, problem):
        self.assistant.reset()
        chat_history = self.ragproxyagent.initiate_chat(self.assistant, message=self.ragproxyagent.message_generator, problem=problem).chat_history

        if chat_history and len(chat_history) > 0:
    # Iterate through the chat history to find the last assistant message.
            last_assistant_message = None
            for message in reversed(chat_history):
                if message.get("name") == "assistant":
                    last_assistant_message = message
                    break
              

        return last_assistant_message["content"] 


# qa_system = QuestionAnsweringSystem()
# question = "Generate BDD for the API  /api/account/pin/update"
# answer = qa_system.answer_question(question)
# print(answer)
 