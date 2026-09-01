import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "datasets" / "cleaned_news.csv"


# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(DATASET_FILE)

X = df["content"]
y = df["label"]

print(f"Total dataset: {len(df)}")


# ==================================================
# HOLD OUT FINAL TEST SET
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training data for CV: {len(X_train)}")
print(f"Final test data: {len(X_test)}")


# ==================================================
# PIPELINE
# ==================================================

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=100000,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LinearSVC(
            random_state=42
        )
    )
])


# ==================================================
# 5-FOLD CROSS VALIDATION
# ==================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = [
    "accuracy",
    "precision",
    "recall",
    "f1"
]

print("\nRunning 5-fold cross-validation...")

results = cross_validate(
    pipeline,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring,
    n_jobs=-1
)


# ==================================================
# RESULTS
# ==================================================

print("\n" + "=" * 50)
print("5-FOLD CROSS-VALIDATION RESULTS")
print("=" * 50)

for metric in scoring:
    scores = results[f"test_{metric}"]

    print(f"\n{metric.upper()}:")
    print(f"  Fold scores: {scores}")
    print(f"  Mean: {scores.mean():.4f}")
    print(f"  Std:  {scores.std():.4f}")