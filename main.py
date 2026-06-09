from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from search import search_courses
import os
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if not os.path.exists("embeddings/courses.db"):
        os.makedirs("embeddings", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        print("Database not found — fetching courses and embedding...")
        subprocess.run(["python3", "fetch_courses.py"], check=True)
        subprocess.run(["python3", "embed.py"], check=True)
        print("Database ready.")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/search")
def search(request: SearchRequest):
    results = search_courses(request.query, request.top_k)
    return {"results": results}

@app.get("/health")
def health():
    return {"status": "ok"}