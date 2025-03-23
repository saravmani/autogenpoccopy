## dependent packages - bs4,duckduckgo_search,bs4,gro, autogen

import os
from dotenv import load_dotenv
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, initiate_chats
from typing import Annotated, Literal
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup 
import requests

load_dotenv() 
 
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  
 
llm_config = {
    "model": "gpt-3.5-turbo", 
    "api_key": OPENAI_API_KEY,
    
    }



 
def web_search(query: Annotated[str, "search query"]) -> str:
    results = DDGS().text(query,max_results=3)
    print(results)
    print('-----------==========------------')
    summaries = []
    for result in results:
        summaries.append(fetch_webpage_content(result['href']))

    print(summaries)
    print('-----------==========------------')
    return "\n".join(summaries)

def fetch_webpage_content(url: str) -> str:
    """Fetch the content of a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join(p.get_text() for p in soup.find_all("p"))
        return text
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"
 
user_proxy = UserProxyAgent( #changed to UserProxyAgent
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",  # changed to NEVER
    code_execution_config=False
)

assistant = AssistantAgent( #changed to assistantAgent
    name="Assistant",
    system_message="You are a helpful assistant. When the user asks a search query, use the web_search function to search, then summarize the results in 2 lines. Return TERMINATE when you are done.",
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"]
)

assistant.register_for_llm(name="web_search", description="Perform a web search and return the top 3 URLs")(web_search)

user_proxy.register_for_execution(name="web_search")(web_search)

user_input = input("Enter your search query: ")

chats = user_proxy.initiate_chat(
    assistant,
    message=user_input,
)

print(chats.summary)    
