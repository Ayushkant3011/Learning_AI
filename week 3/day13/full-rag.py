import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2') #384 length


load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key not Found")
client = Groq(api_key = my_api_key)
groqModel="openai/gpt-oss-20b"


documents = [
    "Employees receive 24 days of paid leave per year.",

    "Employees work from the office on Tuesday, Wednesday and Thursday.",

    "Monday and Friday are optional work-from-home days.",

    "Employees receive Rs.3000 per month for gym reimbursement.",

    "Employees can claim Rs.2000 per month for home internet.",

    "Employees have a 90 day notice period."
]

document_embeddings = model.encode(documents)

def cosine_Similarity(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def retrieve(query_embedding):
    scores = []
    for i, document in enumerate(document_embeddings):
        score = cosine_Similarity(query_embedding, document)
        scores.append((score, documents[i]))
    scores.sort(reverse=True)
    return scores[0]

def askLLM(question,context):

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
    response = client.chat.completions.create(model=groqModel, messages=messages)
    answer = response.choices[0].message.content
    return answer

query = "How much Vacation do I get?"
query_embedding = model.encode(query)

score, context = retrieve(query_embedding)


answer = askLLM(query, context)
print(answer)