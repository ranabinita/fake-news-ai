import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "datasets" / "cleaned_news.csv"


# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(DATASET_FILE)

print(f"Total dataset: {len(df)}")


# ==================================================
# BODY-ONLY DATA
# ==================================================

X = df["text"].fillna("")
y = df["label"]


# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ==================================================
# TF-IDF
# ==================================================

print("\nTraining body-only TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"TF-IDF training shape: {X_train_tfidf.shape}")
print(f"TF-IDF testing shape: {X_test_tfidf.shape}")


# ==================================================
# LINEAR SVM
# ==================================================

print("\nTraining body-only Linear SVM...")

model = LinearSVC(
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# ==================================================
# PREDICTIONS
# ==================================================

y_pred = model.predict(X_test_tfidf)


# ==================================================
# EVALUATION
# ==================================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print("BODY-ONLY LINEAR SVM RESULTS")
print("=" * 50)

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Fake", "Real"]
    )
)

print("Confusion Matrix:")

print(confusion_matrix(y_test, y_pred))