import pandas as pd
from collections import Counter
import os

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/processed/jobs_cleaned.csv")

common_skills = [

    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",

    "machine learning",
    "deep learning",

    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",

    "git",
    "github",

    "java",
    "javascript",
    "react",

    "flask",
    "django",

    "mongodb",
    "mysql",
    "postgresql"
]

skill_counter = Counter()

for _, row in df.iterrows():

    text = str(
        row["description"]
    ).lower()

    for skill in common_skills:

        if skill in text:
            skill_counter[skill] += 1

top_skills = pd.DataFrame(
    skill_counter.items(),
    columns=["Skill", "Count"]
)

top_skills = top_skills.sort_values(
    by="Count",
    ascending=False
)

print("\n===== TOP SKILLS =====\n")

print(
    top_skills.head(20)
)

top_skills.to_csv(
    "data/processed/top_skills.csv",
    index=False
)

print(
    "\nSaved: data/processed/top_skills.csv"
)