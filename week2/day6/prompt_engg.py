import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND !!!!")

client = Groq(api_key = my_api_key)
model="openai/gpt-oss-20b"

def llm_response(prompt):
    message={
        "role":"user",
        "content":prompt
    }

    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)

    ans = response.choices[0].message.content
    return ans

bad_Prompt="""
This is a user complaint:
    My Laptop is not working
    Classfiy this
"""
good_Prompt="""
#ROLE:
Your are a support assistant at a mobile/laptop company
#TASK:
You have to classify the issue in a category
#CONSTRAINT:
You have to classify the issue in one of three categories namely billing, technical, return
#OUTPUT FORMAT: 
Youar answer should be in one world only. the one word should be one of the categories given in constratints
#EXAMPLE:
for instance if a user complaint says he want a refund then the category should be Return
#FALLBACK:
If the issue is unrelated to any of the categories mentuioned in constraints, then the answer should be OTHER
    This is a user complaint:
    My Laptop is not working
"""

print(llm_response(bad_Prompt))

print("######################")

print(llm_response(good_Prompt))