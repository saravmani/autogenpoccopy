import autogen
import requests
import os
from Tools.TestDataGeneratorTool import SwaggerTestDataGenerator

from dotenv import load_dotenv
load_dotenv() 
 
 


config_list = [
    {
    "model": "gpt-3.5", 
    "api_key": os.getenv('OPENAI_API_KEY')  ,
    }
]
 
llm_config = {"config_list": config_list, "cache_seed": 42}
openapi_url = "http://localhost:8080/v3/api-docs"  # Hardcoded URL
 

def extract_and_print():  # URL is now hardcoded
    """Extracts and prints the OpenAPI info."""
    try:
        response = requests.get(openapi_url)
        response.raise_for_status()
        openapi_data = response.json()
        return openapi_data 

    except requests.exceptions.RequestException as e:
        return f"Error fetching OpenAPI document: {e}"
    except ValueError as e:
        return f"Error parsing JSON: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
openapi_expert = autogen.AssistantAgent(
    name="OpenAPIExpert",
    llm_config=llm_config,
    system_message="You are an OpenAPI expert. You extract API path, parameter names, data types, "
    "and expected responses from OpenAPI documents. Call the function `extract_and_print`.",
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
      is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    code_execution_config=False,
    llm_config=llm_config,
)




openapi_expert.register_for_llm(
    name="extract_and_print",
    description="Extracts and prints the OpenAPI info from a hardcoded URL.",
)(extract_and_print)

user_proxy.register_for_execution(name="extract_and_print")(extract_and_print)

user_proxy.initiate_chat(
    openapi_expert,
    message="Extract the API details.",
)