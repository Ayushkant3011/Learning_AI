import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer


def cosine_Similarity(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

model = SentenceTransformer('all-MiniLM-L6-v2') #384 length

text = "Machine Learning is fun"

embedding = model.encode(text)
# print(embedding.shape)
# print(embedding[:10])

t1  = "There are 24 paid leaves"
# t2 = "There are 24 vacation days"
t2 = "I love Pizza"

e1 = model.encode(t1)
e2 = model.encode(t2)

print(cosine_Similarity(e1,e2))