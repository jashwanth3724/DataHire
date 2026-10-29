import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/indian_jobs.csv")

print("Original Rows:", len(df))

# Remove duplicates
df = df.drop_duplicates()

# Fill text columns
text_columns = [
    "title",
    "company",
    "location",
    "description",
    "redirect_url"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("")

# Fill salary columns
if "salary_min" in df.columns:
    df["salary_min"] = df["salary_min"].fillna(0)

if "salary_max" in df.columns:
    df["salary_max"] = df["salary_max"].fillna(0)

# Save cleaned file
df.to_csv(
    "data/processed/jobs_cleaned.csv",
    index=False
)

print("Cleaned Rows:", len(df))
print("Indian jobs saved successfully!")