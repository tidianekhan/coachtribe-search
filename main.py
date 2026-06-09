from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from search import search_courses
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "embeddings", "courses.db")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.join(BASE_DIR, "embeddings"), exist_ok=True)
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
        print("Database not found — fetching and embedding...")
        subprocess.run(["python3", os.path.join(BASE_DIR, "fetch_courses.py")], check=True)
        subprocess.run(["python3", os.path.join(BASE_DIR, "embed.py")], check=True)
        print("Database ready.")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/", response_class=HTMLResponse)
def index():
    with open(os.path.join(BASE_DIR, "templates/index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/search")
def search(request: SearchRequest):
    results = search_courses(request.query, request.top_k)
    return {"results": results}

@app.get("/health")
def health():
    return {"status": "ok"}