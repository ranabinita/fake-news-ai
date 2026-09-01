import os
import joblib

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
MODEL_PATH=os.path.join(
    BASE_DIR,
    "models",
    "fake_news_model.pkl",
)
VECTORIZER_PATH=os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl"
)
model=joblib.load(MODEL_PATH)
vectorizer=joblib.load(VECTORIZER_PATH)
def predict_news(title, text):
    """
    Predict whether a news article is Fake or Real.
    """

    title = title or ""
    text = text or ""

    title = title.strip()
    text = text.strip()

    if not title and not text:
        raise ValueError("News title or text cannot be empty.")

    # Reproduce the exact format used during training
    content = title + " " + text

    # Convert using the trained TF-IDF vectorizer
    text_vector = vectorizer.transform([content])

    # Predict
    prediction = model.predict(text_vector)[0]

    # Convert numerical label to readable result
    label = "Fake" if prediction == 0 else "Real"

    return {
        "prediction": label,
        "label": int(prediction)
    }
