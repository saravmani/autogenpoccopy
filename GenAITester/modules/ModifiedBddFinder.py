
import json
from typing import Annotated
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions 
from utils.file_dif_finder import compare_markdown_files

import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
  
 


llm_config_openApi_with_schema = { 
    "model": "gpt-4o",
    "api_key": OPENAI_API_KEY
}


llm_config_openApi = { 
    "model": "gpt-4o",
    "api_key": OPENAI_API_KEY 
}


llm_config = llm_config_openApi

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-ada-002"
)

def feature_file_Writer(api_url: Annotated[str, "api url"], content: Annotated[str, "BDD Test cases to write"]) -> str:
    cleansed_file_name=api_url.replace("/","_")
    file_path = os.path.join(os.getenv('BDDFILESPATH'), cleansed_file_name+".feature") 
    with open(file_path, 'w') as file:
        file.write(content)
    return "File written successfully."

class ModifiedBddFinder:
    def __init__(self,apiUrl,test_data):
        self.structured_agent = AssistantAgent(
           
             
            name="structured_agent",
            system_message=
             "You are an expert at finding the existing API URLs from the modified content.\n\n"
        "Background:\n"
        "I previously wrote test cases for my Microservice Application based on 'document1'.\n"
        "However, the business analyst has updated the content, creating a new 'document2'.\n"
        "I've determined the differences between 'document1' and 'document2' and provided the modified content below.\n\n"
        "Task:\n"
        "Find ONLY the related impacted API URLs from the context based on the provided content section. You are not going to generate/modify any URL but you are going to just indentify the impacted EXISTING url from the document context.\n\n"
        "You must respond strictly with a JSON structure as follows. dont add any markup.  i want exact json output with all modified urls:\n"
        "{"
        '  "api_urls_with_content_modified": [ {"url": "api url1", "content": "modified content1"}, {"url": "api url2", "content": "modified content2"} ,"..."]'
        "}"
        "Return TERMINATE when done."
            ,
            llm_config=llm_config_openApi_with_schema 
        )

        self.ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            llm_config=llm_config ,
            max_consecutive_auto_reply=1,
            system_message="Assistant who has extra content retrieval power for solving difficult problems",
            code_execution_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],

            retrieve_config={
                "task": "qa",
                "docs_path": os.getenv('MODIFED_FUNCTIONAL_DOCS_PATH'),
                "embedding_function": openai_ef,
                "get_or_create": True,
                "chunk_token_size": 1500,
                "top_k": 2 ,  
                "chunk_overlap": 500,                
                "embedding_model": "text-embedding-ada-002",
                "model":  'gpt-4o', 
                "vector_db": "chroma",
                "overwrite": True,  # set to True if you want to overwrite an existing collection
            
                }
        )
         
        # self.assistant.register_for_llm(name="feature_file_Writer", description="Write the generated BDD test cases into a file")(feature_file_Writer)       
        # self.ragproxyagent.register_for_execution(name="feature_file_Writer")(feature_file_Writer)

    def update_bbd_test_cases(self):        
        self.structured_agent.reset()
        conent_modified = self.get_modified_bdd_files_difference()
        task = "Find the related API Urls related to the content : "+conent_modified
        # chathistory =self.ragproxyagent.initiate_chat(self.structured_agent, message=task).chat_history
        chat_history = self.ragproxyagent.initiate_chat(self.structured_agent, message=self.ragproxyagent.message_generator, problem=task).chat_history
        for msg in self.ragproxyagent.chat_messages[self.structured_agent]:
            if msg.get("content") :
                try:
                    content = msg.get("content")
                    if "api_urls_with_content_modified" in content :                
                        data = json.loads(msg["content"])
                        return data
                except json.JSONDecodeError:
                    print("Received non-JSON response:", msg["content"])

 
    def get_modified_bdd_files_difference(self):
        # We can find the differences from GIT main/develop branch between the functional documents
        # for now i am directly using the files from my hard drive
        file1_path = os.path.join(os.getenv('FUNCTIONAL_DOCS_PATH'),"FunctionalDocument.md")
        file2_path = os.path.join(os.getenv('MODIFED_FUNCTIONAL_DOCS_PATH'),"FunctionalDocumentmodified.md") 
        differences = compare_markdown_files(file1_path, file2_path)
        return differences

