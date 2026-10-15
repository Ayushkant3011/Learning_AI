import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader


load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key = my_api_key)

MODEL="openai/gpt-oss-20b"


BASE_DIR = Path(__file__).resolve().parent

PROMPT_PATH = BASE_DIR / "prompts" / "candidate_system_prompt.txt"


#PARSING RESUME
class Experience(BaseModel):
    company: str | None = None
    role:str | None = None
    duration:str | None = None
    description:str | None = None
    skills_used:str | None = None

class Resume(BaseModel):
    name:str | None = None
    email:str | None = None
    phone:str | None = None

    total_experience_years: float | None = None

    skills: list[str] =[]
    experience: list[Experience] =[]
    education: list[str] =[]
    projects: list[str] =[]
    certifications: list[str] =[]

resume_schema = Resume.model_json_schema()

class ChatRequest(BaseModel):
    question:str


def ask_Candidate(question: str, resume: Resume):
    with open(PROMPT_PATH, "r", encoding="utf-8") as file:
        prompt_template = file.read()
    
    system_prompt=prompt_template.replace(
        "{resume_json}",
        resume.model_dump_json(indent=2)
    )
    response = client.chat.completions.create(
        model=MODEL,

        messages = [
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":question
            }
        ]
    )

    return response.choices[0].message.content



def parse_resume(resume_text):
    system_prompt=f"""
        You are an expert resume parser, 

        Extract information from the resume based on its meaning,
        not only based on exact section headings.

        Different resumes may use different headings.

        For example:
        - Experience
        - Professional Experience
        - Work History
        - Employment
        - Internships

        These may all conatin relevant experience.

        Skills may also appear in the skills section, work experience, internships or projects.

        Return ONLY valid JSON matching this schema:

        {resume_schema}

        Important rules:
        1. Do not invent information
        2. If a value iss not avaiable, return null
        3. If a list has no information, return an empty list
        4. Include internships inside experiences.
        5. Extract skills mentioned across the entire resume.
        
        6. Calculate total_experience_years from the candidate's
            employment dates when sufficient information is available.
        
        7. Use the current date to calculate experience for ongoing roles.
        
        8. Do not count overlapping employment periods twice.
        
        9. If employment dates are insufficient to calculate a
                reliable total, return null.
        
                 
    """

    user_prompt= f"""
        Parse the following Resume:

        {resume_text}
    """

    message_system = {
        "role":"system",
        "content":system_prompt
    }

    message_user={
        "role":"user",
        "content":user_prompt
    }

    messages=[message_system, message_user]
    response_format={
        "type":"json_object"
    }

    response = client.chat.completions.create(
        model=MODEL, 
        messages= messages, 
        response_format = response_format, 
        max_tokens=4096
    )

    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume


#PDF EXTRACTION
def read_pdf(file_path:Path):
    reader = PdfReader(file_path)
    text=""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

from contextlib import asynccontextmanager

resume_data = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global resume_data

    print("Loading and parsing resume...")

    resume_text = read_pdf(Path("Ayush_Kant_Resume.pdf"))
    resume_data = parse_resume(resume_text)

    print("Resume parsed successfully!")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {
        "message": "Resume Parsed Successfully",
        "resume": resume_data.model_dump()
    }


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_Candidate(request.question, resume_data)

    return {
        "answer": answer
    }
