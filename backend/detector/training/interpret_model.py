import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

BASE_DIR =Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR/"datasets"/'cleaned_news.csv'

df=pd.read_csv(DATASET_FILE)
print(f"total dataset: {len(df)}")

X=df["content"].fillna("")
y=df["label"]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.20,random_state=42,stratify=y
)
print(f"training samples: {len(X_train)}")
print(f"testing samples: {len(X_test)}")
print("\n training tf-idf vectorizer...")
vectorizer=TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1,2)
)
X_train_tfidf = vectorizer.fit_transform(X_train)
print(f"tf-idf shape: {X_train_tfidf.shape}")
print("\n training linear SVM...")
model=LinearSVC(
    random_state=42
)
model.fit(X_train_tfidf,y_train)
features_names=vectorizer.get_feature_names_out()
coefficients=model.coef_[0]
fake_indices=coefficients.argsort()[:30]
real_indices=coefficients.argsort()[-30:][::-1]
print("\n"+"="*60)
print("top features associated with fake news")
print("="*60)
for index in fake_indices:
    print(
        f"{features_names[index]:40s}"
        f"{coefficients[index]:.4f}"
    )
print("\n"+"="*60)
print("top features associated with real news")
print("="*60)
for index in real_indices:
    print(
        f"{features_names[index]:40s}"
        f"{coefficients[index]:.4f}"
    )
print("\n interpretability analysis complete.")