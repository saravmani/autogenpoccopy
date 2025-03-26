import os
from dotenv import load_dotenv
from typing import Annotated
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm_config_openApi = {
    # "model": "gpt-3.5-turbo",
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

class BDDSelfHealer:
    def __init__(self):          
        self.assistant = AssistantAgent(
            name="assistant",
              system_message="""You are expert in Updating existing bdd scenarios provided (Existing_BDD_Test_Cases) in gherkin language, 
              based on the modified content (Modified_Conent) provided by the other agent.
            Follow this rule while updating - Dont modify existing scenarios if No relavent content moidfied. You can added new scenarios if really needed for modified content.              
               If you modify any existing scenario then just update and give dont create duplicate scenario.
        Once BDD test cases are updated in gherkin language then CALL the function feature_file_Writer with complete BDD Scenarios (Existing scenarios + Newly added/Modified scenarios)
        and pass the api url and Complete BDD test cases as arguments.

            Return TERMINATE when you are done """,
            llm_config=llm_config 
        )

        self.ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            llm_config=llm_config ,
            max_consecutive_auto_reply=2,
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
        
        
        self.assistant.register_for_llm(name="feature_file_Writer", description="Write the generated BDD test cases into a file")(feature_file_Writer)       
        self.ragproxyagent.register_for_execution(name="feature_file_Writer")(feature_file_Writer)

    def generate_bdd_test_cases(self, problem):        
        self.assistant.reset()
        chat_history = self.ragproxyagent.initiate_chat(self.assistant, message=self.ragproxyagent.message_generator, problem=problem).chat_history
 
    def feature_file_reader(self,file_name: Annotated[str, "file name"]) -> str:
        file_path = os.path.join(os.getenv('BDDFILESPATH'), file_name)
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    def heal_bdd_files(self,bdd_files_needs_to_be_updated):
        for bdd_modificatioon_context in bdd_files_needs_to_be_updated['api_urls_with_content_modified']:
            self.assistant.reset()
            api_url = bdd_modificatioon_context['url']
            cleansed_file_name=api_url.replace("/","_")
            file_content = self.feature_file_reader(cleansed_file_name+".feature")
            modified_content = bdd_modificatioon_context['content']
            query = "modify the below mentioned BDD test cases and according the givent Modified_Conent -  "+modified_content
            query = query+"\n API Url - "+ api_url
            query = query+"\n Existing_BDD_Test_Cases - "+ file_content
            chat_history = self.ragproxyagent.initiate_chat(self.assistant, message=self.ragproxyagent.message_generator, problem=query)


# qa_system = BDDSelfHealer()
# question = "Generate BDD for the API  /api/account/pin/update"
# answer = qa_system.generate_bdd_test_cases(question)
# print(answer)
  