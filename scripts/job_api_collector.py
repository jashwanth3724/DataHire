import requests
import pandas as pd
import os
import time

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
print(APP_ID)
print(APP_KEY)

os.makedirs("data/raw", exist_ok=True)

jobs = []

searches = [
    ("Data Analyst", "Bangalore"),
    ("Data Scientist", "Hyderabad"),
    ("Business Analyst", "Pune"),
    ("Python Developer", "Chennai"),
    ("Machine Learning Engineer", "Mumbai"),
    ("Data Analyst", "Noida"),
    ("Data Scientist", "Gurgaon")
]

for role, city in searches:

    print(f"Fetching {role} jobs in {city}...")

    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what={role}"
        f"&where={city}"
        f"&results_per_page=50"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed:", response.status_code)
        continue

    data = response.json()

    for job in data.get("results", []):

        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "location": city,
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "description": job.get("description", ""),
            "redirect_url": job.get("redirect_url", "")
        })

    time.sleep(1)

df = pd.DataFrame(jobs)

df.to_csv(
    "data/raw/indian_jobs.csv",
    index=False
)

print("\n====================")
print(f"Collected {len(df)} jobs")
print("Saved: data/raw/indian_jobs.csv")
print("====================")