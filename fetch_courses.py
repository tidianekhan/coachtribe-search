import requests
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def strip_html(html):
    return re.sub(r'<[^>]+>', '', html).strip()

def fetch_courses():
    url = "https://coachtribe.nl/wp-json/wp/v2/sfwd-courses"
    params = {"per_page": 100}
    
    response = requests.get(url, params=params, auth=(WP_USER, WP_APP_PASSWORD))
    response.raise_for_status()
    
    raw_courses = response.json()
    courses = []
    
    for course in raw_courses:
        description = strip_html(course["content"]["rendered"]).strip()
        courses.append({
            "id": course["id"],
            "title": course["title"]["rendered"],
            "description": description,
            "url": course["link"]
        })
    
    with open("data/courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(courses)} courses")
    
    # Flag thin descriptions
    thin = [c for c in courses if len(c["description"]) < 50]
    if thin:
        print(f"\nWarning: {len(thin)} courses have thin descriptions:")
        for c in thin:
            print(f"  - {c['title']}: '{c['description']}'")

if __name__ == "__main__":
    fetch_courses()