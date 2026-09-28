import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND !!!!")

client = Groq(api_key = my_api_key)
# model="openai/gpt-oss-20b"
model="qwen/qwen3.8-27b"

#Tools
def get_product_price(product):
    if product == 'iPhone 17' : return 1000

    elif product == 'iPhone 15' : return 500

    else : return 0


def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Calc Error!"

tools={
    "get_product_price" : get_product_price,
    "calculator" : calculator
}

system_prompt="""
    You are a Shopping Assistant.

    You have these Tools:
    get_product_price(product)
    calculator(expression)

    IMPORTANT:
    Call tools exactly like these examples:

    Action: get_product_price("iPhone 17")
    Action: calculator("5000 - 2000")

    Never Write:
    get_product_price(product="iPhone 17")

    Never Write:
    calculator(expression="5000 - 2000")

    Follow These Rules:

    1. Decide what you need to do next
    2. Call ONLY ONE tool at a time
    3. After writing an Action, STOP Immediately
    4. Never guess or invent a tool result
    5. Wait until you receive an Observation
    6. Then decide your next action
    7. When the task is complete, give the Final Answer.

    Format:

    thought: what you need to do 
    Action: tool_name(argument)

    When Finished:
    Final Answer: Your Answer
"""


def run_Agent(question):
    messages = [
        {
            "role":"system",
            "content": system_prompt
        },
        {
            "role":"user",
            "content":question
        }
    ]

    for step in range(5):
        print("\n----------------------") 
        print("STEP", step +1) 
        print("----------------------")

        response= client.chat.completions.create(
            model=model,
            messages = messages,
            temperature=0,
        ) 

        answer = response.choices[0].message.content

        print(answer)

        # Agent has finished
        if "Final Answer:" in answer: break

        #Find the Action
        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )

        if match:
            tool_name = match.group(1)

            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

            # RUn the Tool
            if tool_name in tools:

                tool = tools[tool_name]

                observation = tool(tool_input)

            else:
                observation = "Tool Not Found"

            print("Observation", observation)


            # Add LLM response to Memory
            messages.append({
                "role":"assistant",
                "content" : answer
            })

            #Give tool result back to LLM
            messages.append({
                "role":"user",
                "content":
                    "Observation: " 
                    + str(observation)
            })

            sleep(5)




prompt="""
    I have 5000 rupees, What is the price of an iPhone 17?
    and how much money will i have left if i decide to buy it?
"""

run_Agent(prompt)