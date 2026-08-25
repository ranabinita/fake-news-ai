import pandas as pd
from pathlib import Path


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "datasets" / "cleaned_news.csv"


# Load cleaned dataset
df = pd.read_csv(DATASET_FILE)

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)

print(f"Total articles: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

print("\nClass distribution:")
print(df["label"].value_counts())

print("\nClass percentages:")
print(df["label"].value_counts(normalize=True).mul(100).round(2))


# Check missing values
print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(df.isnull().sum())


# Check exact duplicates
print("\n" + "=" * 50)
print("DUPLICATES")
print("=" * 50)

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate content:", df["content"].duplicated().sum())


# Content length
df["content_length"] = df["content"].str.len()

print("\n" + "=" * 50)
print("CONTENT LENGTH")
print("=" * 50)

print(df["content_length"].describe())


# Very short content
print("\nContent shorter than 100 characters:",
      (df["content_length"] < 100).sum())

print("Content shorter than 500 characters:",
      (df["content_length"] < 500).sum())


# Class-specific content length
print("\nAverage content length by class:")

print(
    df.groupby("label")["content_length"]
    .mean()
    .round(2)
)


# Show very short examples
print("\n" + "=" * 50)
print("VERY SHORT EXAMPLES")
print("=" * 50)

short_articles = df[df["content_length"] < 100]

print(short_articles[["content", "label"]].head(10).to_string())


print("\nEDA complete.")