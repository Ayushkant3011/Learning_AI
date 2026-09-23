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


# Structure the output
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    contact:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
    Extract the personal information from the ticket strictly based on this schema and give a json output
    {schema}
"""

message_system={
    "role":"system",
    "content":system_prompt
}

text="Hello my name is Ayush. I have an iphone which is not working at all right now, My address is Noida, my email is ayush@gmail.com and my contact number is 1234567890"


prompt=f"""
    This is a customer ticket and please extract the personal information from this.
    {text}
"""
message={
    "role": role,
    "content":prompt
}

messages=[message_system, message]

response=client.chat.completions.create(model=model, messages= messages, response_format=response_format)


answer = response.choices[0].message.content
print(answer)



# how to read this
import json
raw_json = answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)