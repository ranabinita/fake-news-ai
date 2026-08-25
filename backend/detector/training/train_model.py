import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.svm import LinearSVC

BASE_DIR =Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR/"datasets"/"cleaned_news.csv"

df = pd.read_csv(DATASET_FILE)
print(f"total dataset: {len(df)}")
X = df["content"]
y=df["label"]

X_train,X_test, y_train,y_test= train_test_split(
    X,y,test_size=0.20,random_state=42,stratify=y
)
print(f"training samples:{len(X_train)}")
print(f"testing samples:{len(X_test)}")
print("\n training TF-IDF vectorizer...")
vectorizer=TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1,2)
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("\n training class distribution:")
print(y_train.value_counts())
print("\n testing class distribution:")
print(y_test.value_counts())
print(f"TF-IDF training shape: {X_train_tfidf.shape}")
print(f"TF-IDF testing shape: {X_test_tfidf.shape}")


# Logistic Regression
print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# Predictions
y_pred = model.predict(X_test_tfidf)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print("LOGISTIC REGRESSION RESULTS")
print("=" * 50)

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Fake", "Real"]
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# ==================================================
# LINEAR SVM
# ==================================================

print("\nTraining Linear SVM...")

svm_model = LinearSVC(
    random_state=42
)

svm_model.fit(X_train_tfidf, y_train)

# Predictions
svm_pred = svm_model.predict(X_test_tfidf)

# Evaluation
svm_accuracy = accuracy_score(y_test, svm_pred)

print("\n" + "=" * 50)
print("LINEAR SVM RESULTS")
print("=" * 50)

print(f"Accuracy: {svm_accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    svm_pred,
    target_names=["Fake", "Real"]
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, svm_pred))