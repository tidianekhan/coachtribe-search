import sqlite3
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_courses(query, top_k=5):
    query_embedding = np.array(get_embedding(query), dtype=np.float32)

    conn = sqlite3.connect("embeddings/courses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, url, embedding FROM courses")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        id, title, description, url, embedding_bytes = row
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        score = cosine_similarity(query_embedding, embedding)
        results.append({
            "id": id,
            "title": title,
            "description": description,
            "url": url,
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    query = input("Zoekterm: ")
    results = search_courses(query)
    for r in results:
        print(f"\n{r['title']} (score: {r['score']:.3f})")
        print(f"{r['description'][:100]}...")
        print(f"{r['url']}")