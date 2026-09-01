import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "cleaned_news.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

X = df["content"]
y = df["label"]

print("Total dataset:", len(df))


# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

print("\nTraining final TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_tfidf = vectorizer.fit_transform(X)

print("TF-IDF shape:", X_tfidf.shape)


# --------------------------------------------------
# FINAL MODEL
# --------------------------------------------------

print("\nTraining final Linear SVM...")

model = LinearSVC(
    random_state=42
)

model.fit(X_tfidf, y)

print("Final model training complete.")


# --------------------------------------------------
# SAVE ARTIFACTS
# --------------------------------------------------

vectorizer_path = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.pkl"
)

model_path = os.path.join(
    MODEL_DIR,
    "fake_news_model.pkl"
)

joblib.dump(vectorizer, vectorizer_path)
joblib.dump(model, model_path)


print("\n==================================================")
print("MODEL SAVING COMPLETE")
print("==================================================")

print("Vectorizer saved to:")
print(vectorizer_path)

print("\nModel saved to:")
print(model_path)