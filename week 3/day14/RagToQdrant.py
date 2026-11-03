# PART 1 - IMPORTS

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not Found")
groqModel="openai/gpt-oss-20b"

# Connect to QDRANT
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

print("Connected to Qdrant Cloud!!")


#Create QDRANT Collection

COLLECTION_NAME = "Knowledge"
EMBEDDING_SIZE = 384

#Delete Collection if already exists
if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting Existing Collection: {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)

#CREATE COllection
client.create_collection(
    collection_name = COLLECTION_NAME,
    vectors_config = VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE
    ),
)


print(f"Created Collection: {COLLECTION_NAME}")
print(f"Vector Size : {EMBEDDING_SIZE}")
print("Distance : COSINE")



#Load Our Knowledge
with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [
        line.strip()
        for line in f 
        if line.strip()
    ]


print(f"Loaded {len(documents)} documents")


#CREATE EMBEDDINGS

print("Loading Embedding Model..........")

model = SentenceTransformer('all-MiniLM-L6-v2') #384 length

print("Embedding Model Ready!")

embeddings = model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size : {len(embeddings[0])}")


#CREATE QDRANT POINTS

points =[]

for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id = i+1,

        vector = embedding.tolist(),

        payload={
            "text":documents[i]
        }
    )

    points.append(point)



#UPLOAD TO QDRANT
# upsert = upload + insert
client.upsert(
    collection_name = COLLECTION_NAME,
    points = points
)

print(f"Uploaded {len(points)} documents to Qdrant!!")


#SEARCH QDRANT

def search(query, top_k=3):

    #Convert the question to embedding
    query_vector = model.encode(query).tolist()

    #Search Qdrant
    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_k,
        with_payload = True
    ).points

    return results



#TEST SEARCH
query = "How many vacation days do I get?"

results = search(query, top_k=3)

print("\nSearch Results: ")

for result in results:
    print(f"Score: {result.score: .3f}")
    print(result.payload["text"])
    print()


#CONNECT TO GRQO

groqClient = Groq(api_key = GROQ_API_KEY)


def askLLM(question, context):
    prompt=f"""
    Asnwer the question using only the information provided below

    Context: {context}

    Question: {question}

    If the answer is not present in the context, say "I dont know based on the provided information.
    """

    response = groqClient.chat.completions.create(
        model = groqModel,
        messages =[
            {
                "role":"user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content




#COMPLETE RAG PIPELINE

question = "How Many vacation days do I get?"

results = search(question, top_k=3)

#Extract text from the search resulsts
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = askLLM(question, context)

print("\nFinal Answer: ")
print(answer)