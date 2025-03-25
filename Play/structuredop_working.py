import autogen
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Create structured_agent WITHOUT functions
structured_agent = autogen.AssistantAgent(
    name="StructuredAgent",
    system_message=(
        "You must reply strictly with JSON formatted like this:\n"
        "{\n"
        '  "name": "<full name>",\n'
        '  "age": <age>,\n'
        '  "occupation": "<occupation>",\n'
        '  "interests": ["interest1", "interest2", "..."]\n'
        "}"
    ),
    llm_config={
        "config_list": [
            {"model": "gpt-3.5-turbo", "api_key": openai.api_key}
        ]
    }
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=1,
    llm_config={
        "config_list": [
            {"model": "gpt-3.5-turbo", "api_key": openai.api_key}
        ]
    }
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, structured_agent],
    messages=[],
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False
)

manager = autogen.GroupChatManager(groupchat=groupchat)

# Initiate conversation
chat_result = user_proxy.initiate_chat(
    manager,
    message="Provide information about Priya, a 25-year-old software developer interested in writing, music, and traveling."
)

 

# Print structured JSON from the assistant’s response
for msg in structured_agent.chat_messages[user_proxy]:
    if msg.get("content"):
        try:
            data = json.loads(msg["content"])
            print("Structured Output (JSON):")
            print(json.dumps(data, indent=2))
        except json.JSONDecodeError:
            print("Received non-JSON response:", msg["content"])
