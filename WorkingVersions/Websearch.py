## dependent packages - bs4,duckduckgo_search,bs4,gro, autogen

import os
from dotenv import load_dotenv
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, initiate_chats
from typing import Annotated, Literal
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup 
import requests

load_dotenv() 
 
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  
 
# llm_config_openApi = {
#     "model": "gpt-3.5-turbo", 
#     "api_key": OPENAI_API_KEY,
#     "cache": None
#     }

llm_config_graq={
     "model": "llama3-8b-8192",
        "api_key": os.getenv('GROQ_API_KEY'),
        "api_type": "groq",
}

llm_config=llm_config_graq
 
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
 
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode = "TERMINATE"
) 
 
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful to perform the websearch and summarise the search result in 2 lines. Return TERMINATE when you are done",
    llm_config=llm_config ,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"]
)


assistant.register_for_llm(name="web_search", description="Perform a web search and return the top 3 URLs")(web_search)
 
user_proxy.register_for_execution(name="web_search")(web_search)


# Start the conversation
chats = user_proxy.initiate_chat(
    assistant,
    message="Search latest news in inida",  # User input
)

print(chats.summary)    
