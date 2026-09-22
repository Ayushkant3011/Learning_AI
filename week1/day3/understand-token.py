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

# # prompts
prompt1="Hi1"
prompt2="Explain time travel in detail under 100 words"
prompt3="Write a 500 word essay on Machine learning"

prompts=[prompt1, prompt2, prompt3]
for prompt in prompts:
    message={
        "role":role,
        "content":prompt
    }
    messages=[message]
    response=client.chat.completions.create(model=model, messages=messages, max_tokens=5000)
    usage=response.usage
    print(f"propmt:{prompt} ---> your tokens:{usage.prompt_tokens} completion_token:{usage.completion_tokens} total Token:{usage.total_tokens} Finish Reason:{response.choices[0].finish_reason}")


# prompt="Suggest a name for my clothing company"
# message={
#     "role": role,
#     "content":prompt
# }

# message_system = {
#     "role": "system",
#     "content": "You are Brand Manager who suggests name for my company. Name should be in one word"
# }

# messages=[message_system, message]

# # By default the temparature is 0 meaning safe response, raneg is [0-2]

# response=client.chat.completions.create(model=model, messages= messages, temperature=1)
# print(response)

print("############ RESPONSE ##################")

# answer = response.choices[0].message.content
# print(answer)