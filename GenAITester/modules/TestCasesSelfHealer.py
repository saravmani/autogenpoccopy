import os
from dotenv import load_dotenv
from typing import Annotated
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



def file_Writer(api_url: Annotated[str, "api url"], content: Annotated[str, "Python test cases"]) -> str:
    cleansed_file_name=api_url.replace("/","_")
    file_path = os.path.join(os.getenv('BDDFILESPATH'), cleansed_file_name+"_test.py") 
    with open(file_path, 'w') as file:
        file.write(content)
    return "File written successfully."

class TestCasesSelfHealer:
    def __init__(self):          
        self.assistant = AssistantAgent(
            name="assistant",
              system_message="""You are expert in Updating existing python test cases based on proided modified modified related bdd test Scenarios(Modified_Related_BDD_Test_Cases) 
              and provided EXISTING python test cases (python_test_file_content_needs_to_be_updated)  ,  

              based on the modified content (Modified_Conent) provided by the other agent.
            Follow this rule while updating - Dont modify existing test cases if No relavent content/ BDD test scenarios moidfied. You can added new test cases if really needed for modified content/  BDD test scenarios .              
               If you modify any existing test cases then just update and dont create duplicate test cases.
        Once python test cases are updated in  then CALL the function file_Writer with complete test cases (Existing test cases + Newly added/Modified test cases )
        and pass the api url and Complete test cases as arguments.

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
        
        
        self.assistant.register_for_llm(name="file_Writer", description="Write the generated/updated python test cases into a file")(file_Writer)       
        self.ragproxyagent.register_for_execution(name="file_Writer")(file_Writer)

   
 
    def file_reader(self,file_name: Annotated[str, "file name"]) -> str:
        file_path = os.path.join(os.getenv('BDDFILESPATH'), file_name)
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    def heal_test_files(self,files_needs_to_be_updated):
        for bdd_modificatioon_context in files_needs_to_be_updated['api_urls_with_content_modified']:
            self.assistant.reset()
            api_url = bdd_modificatioon_context['url']
            cleansed_file_name=api_url.replace("/","_")
            feature_file_content = self.file_reader(cleansed_file_name+".feature")
            test_file_content = self.file_reader(cleansed_file_name+"_test.py")
            modified_content = bdd_modificatioon_context['content']
            query = "modify the below mentioned python test cases (test_file_content_needs_to_be_updated) and according the modified related bdd test cases (Modified_Related_BDD_Test_Cases) givent Modified_Conent -  "+modified_content
            query = query+"\n API Url - "+ api_url
            query = query+"\n Modified_Related_BDD_Test_Cases - "+ feature_file_content
            query = query+"\n python_test_file_content_needs_to_be_updated - "+ test_file_content
            self.ragproxyagent.initiate_chat(self.assistant, message=self.ragproxyagent.message_generator, problem=query)


# qa_system = BDDSelfHealer()
# question = "Generate BDD for the API  /api/account/pin/update"
# answer = qa_system.generate_bdd_test_cases(question)
# print(answer)
  
  