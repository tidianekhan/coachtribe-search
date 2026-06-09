# CoachTribe Search

AI-powered semantic search engine for the CoachTribe course library.

Built as a decoupled Python service — entirely separate from WordPress — and designed to be mounted on the CoachTribe platform via a single API endpoint.

---

## How it works

Rather than matching keywords, the search engine understands the intent behind a query. Each course description is converted into a vector (a numerical representation of its meaning) using OpenAI's `text-embedding-3-small` model. When a member searches, the query is embedded the same way and compared mathematically against all course vectors. The closest matches are returned as ranked results.

A member searching for "hoe help ik een cliënt die vastloopt" will find the right course even if those exact words don't appear in any course title or description.

---

## Stack

- **FastAPI** — serves the search endpoint and demo UI
- **OpenAI** `text-embedding-3-small` — generates embeddings
- **SQLite** — stores course data and vectors locally
- **Python 3**

---

## Project structure

```
coachtribe-search/
├── data/
│   └── courses.json        # Course data pulled from WordPress (not committed)
├── embeddings/
│   └── courses.db          # SQLite database with vectors (not committed)
├── templates/
│   └── index.html          # Demo UI
├── fetch_courses.py        # Pulls courses from WordPress REST API
├── embed.py                # Embeds courses and stores in SQLite
├── search.py               # Cosine similarity search logic
├── main.py                 # FastAPI app
├── .env                    # API keys (not committed)
└── requirements.txt        # Dependencies
```

---

## Setup

**1. Clone the repo and create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip3 install -r requirements.txt
```

**3. Add environment variables**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key
WP_USER=your_wordpress_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

**4. Fetch courses from WordPress**

```bash
python3 fetch_courses.py
```

**5. Generate embeddings**

```bash
python3 embed.py
```

**6. Run the server**

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` for the demo UI or `http://localhost:8000/health` to verify the service is running.

---

## API

**POST** `/search`

Request:
```json
{
  "query": "hoe start ik een coachpraktijk",
  "top_k": 5
}
```

Response:
```json
{
  "results": [
    {
      "id": 9429,
      "title": "Het fundament onder een gezonde coachpraktijk: jouw niche",
      "description": "...",
      "url": "https://coachtribe.nl/courses/...",
      "score": 0.577
    }
  ]
}
```

---

## Generating requirements.txt

```bash
pip3 freeze > requirements.txt
```

---

## Notes

- Three courses currently have thin or missing descriptions: *Meester In Herkaderen*, *Mindfulness*, *Vitaal Ouder Worden*. These will embed poorly until descriptions are added in WordPress.
- The embedding step only needs to be re-run when courses are added or descriptions change.
- The `.env` file and generated database are excluded from version control and must be recreated locally.