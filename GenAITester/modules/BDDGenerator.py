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

class BddGenerator:
    def __init__(self,apiUrl,test_data):
        self.assistant = AssistantAgent(
            name="assistant",
            system_message="""You are expert in writting BDD Test cases in gherkin language, for the API with the given context, API parameters, API information 
            Get the information from the context Generate the requested content based on the context. Dont provide anything Extra. Only provide the details for the Given API URL - """+apiUrl+
            """Also you have to write the test cases in gherkin language and validate the test cases are in  gherkin language before responding
            The test cases should be Autonomous and independent. 
            If required have presetup Ex: For duplicate/existing check condition as part of setup create first then create second time.
            Sample Test Data: """+test_data+"""
Once BDD test cases are generated in gherkin language then CALL the function feature_file_Writer 
        and pass the api url and BDD test cases as arguments.

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
                # "docs_path": "https://raw.githubusercontent.com/saravmani/mycloud/refs/heads/master/Rem/FunctionalDocument.md",        
                "docs_path": os.getenv('FUNCTIONAL_DOCS_PATH'),
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
        
        
        # Once BDD test cases are generated in gherkin language then CALL the function feature_file_Writer 
        # and pass the api url and BDD test cases as arguments.
        self.assistant.register_for_llm(name="feature_file_Writer", description="Write the generated BDD test cases into a file")(feature_file_Writer)       
        self.ragproxyagent.register_for_execution(name="feature_file_Writer")(feature_file_Writer)

    def generate_bdd_test_cases(self, problem):
        
        self.assistant.reset()
        chat_history = self.ragproxyagent.initiate_chat(self.assistant, message=self.ragproxyagent.message_generator, problem=problem).chat_history

    #     if chat_history and len(chat_history) > 0:
    # # Iterate through the chat history to find the last assistant message.
    #         last_assistant_message = None
    #         for message in reversed(chat_history):
    #             if message.get("name") == "assistant":
    #                 last_assistant_message = message
    #                 break
    #         if last_assistant_message and last_assistant_message.get("content"):
    #                 return last_assistant_message["content"]
    #         else:
    #             return ""


# qa_system = QuestionAnsweringSystem()
# question = "Generate BDD for the API  /api/account/pin/update"
# answer = qa_system.answer_question(question)
# print(answer)
 