import os
from dotenv import load_dotenv
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
            Return TERMINATE when you are done """,
            llm_config=llm_config 
        )

        self.ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=2,
            system_message="Assistant who has extra content retrieval power for solving difficult problems",
            code_execution_config=False,
             is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],

            retrieve_config={
                "task": "qa",
                # "docs_path": "https://raw.githubusercontent.com/saravmani/mycloud/refs/heads/master/Rem/FunctionalDocument.md",        
                "docs_path": "./documents",
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

    def generate_bdd_test_cases(self, problem):
        
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
 