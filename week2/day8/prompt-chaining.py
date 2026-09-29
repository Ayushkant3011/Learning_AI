import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND !!!!")

client = Groq(api_key = my_api_key)
model="openai/gpt-oss-20b"


 
JD= """
    we are hiring a Backend Python Developer

    Requirements:
    - Stong Python
    - Fast API or Django
    - PostgreSQL
    - Docker
    - AWS
    - REST APIs
    - 2+ years of experience
"""

RESUME="""
    Name: Rahul Sharma

    Experience: 3 Years as a Software Developer

    Skills:
    Python, FastAPI, MySQL, Docker, REST APIs, Git

    Projects:
    Build a food delivery backend using FastAPI and MySQL
    
    Deployed Applications using Docker
"""

def askLLM(system_prompt, user_prompt):
    system_message ={
        "role":"system",
        "content":system_prompt
    }
    user_msg ={
        "role":"user",
        "content":user_prompt
    }

    messages = [system_message, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer


def step1_res_extract(RESUME):
    print("STEP 1")
    sys_prompt="""
        You are a professional HR Assistant. Extract the skills from the candidates resume provided.
        Only return the skills no other infomartion. Do not invent any skills by yourself.
        Output Format:
                Skills should be seperated by commas, Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
        Extract the skills from this resume
        {RESUME}
    """

    return askLLM(sys_prompt, user_prompt) 

def step2_JD_extract(JD):
    print("STEP 2")
    sys_prompt="""
        You are a professional HR Assistant. Extract the skills from the Job Description  provided.
        Only return the skills no other infomartion. Do not invent any skills by yourself.
        Output Format:
        Skills should be seperated by commas, Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
        Extract the skills from this jd
        {JD}
    """

    return askLLM(sys_prompt, user_prompt) 

def step3_match(candidate, jd):
    print("STEP 3")
    sys_prompt="""
            You are a professional HR Assistant. Compare the skills of candidate and the skills required in the JD and 
            produce a fianl score between 1 and 100. Also produce a short verdict whether the candidate is a good fit for the role.
    """

    user_prompt=f"""
            Compare and match the skills
            JD: {jd}

            candidate: {candidate}
    """

    return askLLM(sys_prompt, user_prompt)


candidate = step1_res_extract(RESUME)
print(candidate)
sleep(2)
jd = step2_JD_extract(JD)
print(jd)
sleep(2)
score = step3_match(candidate, jd)
print(score)
