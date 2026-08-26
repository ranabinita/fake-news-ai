import pandas as pd
import re
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "datasets" / "cleaned_news.csv"

df = pd.read_csv(DATASET_FILE)

print(f"Total dataset: {len(df)}")


def remove_source_artifacts(text):
    text = str(text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove common image/media markers
    patterns = [
        r"\[video\]",
        r"\[image\]",
        r"featured image",
        r"getty images?",
        r"image courtesy",
        r"photo courtesy",
        r"watch:",
    ]

    for pattern in patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # Remove explicit Reuters references
    text = re.sub(r"\breuters\b", " ", text, flags=re.IGNORECASE)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

print("\nRemoving obvious source artifacts...")

df["clean_content"] = df["content"].fillna("").apply(remove_source_artifacts)

print("Source artifact cleaning complete.")


X = df["clean_content"]
y = df["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


print("\nTraining source-cleaned TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"TF-IDF training shape: {X_train_tfidf.shape}")
print(f"TF-IDF testing shape: {X_test_tfidf.shape}")


print("\nTraining source-cleaned Linear SVM...")

model = LinearSVC(
    random_state=42
)

model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("SOURCE-CLEANED LINEAR SVM RESULTS")
print("=" * 60)

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Fake", "Real"]
    )
)