
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key = my_api_key)

model="openai/gpt-oss-20b"


# Step 1
Knowledge_base={
    "age":"The Age of Ayush is 22 Years",
    "net worth":"The net worth of Ayush is around 50k"
}
# Step 2 - Retreival
def retrieve_info(question):
    question= question.lower()
    if "age" in question: return Knowledge_base["age"]

    elif "net worth" in question : return Knowledge_base["net worth"]

    else : return None


def askLLM(question):
    context = retrieve_info(question)

    sys_prompt=f"""Answer in One line only. And Answer only based on this context. do not hallucinate. Context : {context}"""
    system_message = {
        "role":"system",
        "content":sys_prompt
    }
    message={
        "role":"user",
        "content": question
    }

    messages = [system_message, message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

question="How Rich is Ayush"
print(askLLM(question))