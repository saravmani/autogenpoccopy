import os
from dotenv import load_dotenv
from typing import Annotated
from autogen import AssistantAgent,UserProxyAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm_config_openApi = {
    "model": "gpt-3.5-turbo",
    "api_key": OPENAI_API_KEY
}

llm_config = llm_config_openApi

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-ada-002"
)

def feature_file_Reader(file_name: Annotated[str, "feature file name"]) -> str:
    file_path = os.path.join(os.getenv('BDDFILESPATH'), file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        return content
def feature_file_Writer(file_name: Annotated[str, "feature file name"], content: Annotated[str, "BDD Test cases to write"]) -> str:
    file_path = os.path.join(os.getenv('BDDFILESPATH'), file_name)
    with open(file_path, 'w') as file:
        file.write(content)
    return "File written successfully."

class BDDValidator:
    def __init__(self):
        
        feature_files_list = ",".join(os.listdir(os.getenv('BDDFILESPATH'))) 
        self.user_proxy = UserProxyAgent( 
            name="User",
            llm_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            human_input_mode="TERMINATE",
            code_execution_config=False
        )

        self.feature_file_finder = AssistantAgent(
                    name="feature_file_finder",
                    function_map={"feature_file_Reader": feature_file_Reader},
                    system_message="""
                    You are an expert in finding the file name from the given text content and using the feature_file_Reader function to read the file content.
                    From the user, try to get more details to collect the exact file name.
                    BDD feature files list: """+feature_files_list+"""
                    Once you identify the file name, call the feature_file_Reader function with the filename.
                    After modifying the BDD test cases in the feature file, call the feature_file_Writer function with the filename and the EXACT modified BDD Test cases to update the file.

                    Return TERMINATE when you are done
                    """,
                    llm_config=llm_config ,
                    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
                    max_consecutive_auto_reply=10
                )

     
        self.feature_file_update_agent = AssistantAgent(
            name="feature_file_update_agent",
            function_map={"feature_file_Reader": feature_file_Reader},
            system_message="""
            You are an expert in finding the file name from the given text content and using the feature_file_Reader function to read the file content.
            From the user, try to get more details to collect the exact file name.
            BDD feature files list: """+feature_files_list+"""
            Once you identify the file name, call the feature_file_Reader function with the filename.
            After modifying the BDD test cases in the feature file, call the feature_file_Writer function with the filename and the EXACT modified BDD Test cases to update the file.

            Return TERMINATE when you are done
            """,
            llm_config=llm_config ,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            max_consecutive_auto_reply=10
        )
 
            
        self.feature_file_finder.register_for_llm(name="feature_file_Reader", description="Read the file content and return the content by given feature file name. Ex: filename.feature")(feature_file_Reader)
        self.feature_file_finder.register_for_llm(name="feature_file_Writer", description="Write the given content to the file. Ex: filename.feature , content")(feature_file_Writer)


        self.user_proxy.register_for_execution(name="feature_file_Reader")(feature_file_Reader)
        self.user_proxy.register_for_execution(name="feature_file_Writer")(feature_file_Writer)

    def update_bdd(self):
        while True:
            user_input = input("Do you want help in correcting the BDD test cases? Enter the details with specific file details. (type 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
        
            self.user_proxy.initiate_chat(
                self.feature_file_finder,
                message=user_input,
            )
 

# bdd_validator = BDDValidator()
# bdd_validator.update_bdd();
 
 