import json
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

def embed_courses():
    with open("data/courses.json", "r", encoding="utf-8") as f:
        courses = json.load(f)

    conn = sqlite3.connect("embeddings/courses.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            url TEXT,
            embedding BLOB
        )
    """)

    for course in courses:
        text = f"{course['title']}. {course['description']}"
        embedding = get_embedding(text)
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()

        cursor.execute("""
            INSERT OR REPLACE INTO courses (id, title, description, url, embedding)
            VALUES (?, ?, ?, ?, ?)
        """, (course["id"], course["title"], course["description"], course["url"], embedding_bytes))

        print(f"Embedded: {course['title']}")

    conn.commit()
    conn.close()
    print("\nDone. All courses embedded and stored.")

if __name__ == "__main__":
    embed_courses()