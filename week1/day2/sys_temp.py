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
role="user"
prompt="Suggest a name for my clothing company"
message={
    "role": role,
    "content":prompt
}

message_system = {
    "role": "system",
    "content": "You are Brand Manager who suggests name for my company. Name should be in one word"
}

messages=[message_system, message]

# By default the temparature is 0 meaning safe response, raneg is [0-2]

response=client.chat.completions.create(model=model, messages= messages, temperature=1)
# print(response)

print("############ RESPONSE ##################")

answer = response.choices[0].message.content
print(answer)