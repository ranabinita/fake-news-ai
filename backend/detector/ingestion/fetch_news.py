import os
import requests
from dotenv import load_dotenv
from django.utils.dateparse import parse_datetime
from detector.inference.predict import predict_news
from detector.models import NewsPrediction

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def fetch_news(country="us", page_size=10):
    """
    Fetch current news headlines from NewsAPI.
    """

    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not configured.")

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": page_size,
    }

    response = requests.get(
        NEWS_API_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise ValueError(
            data.get("message", "NewsAPI request failed.")
        )

    return data.get("articles", [])

def analyze_and_save_news(articles):
    saved_predictions=[]
    for article in articles:
        url=(article.get("url")or "").strip()
        if not url:
            continue
        if NewsPrediction.objects.filter(url=url).exists():
            continue
        title=(article.get("title")or "").strip()
        description = (article.get("description")or"").strip()
        if not title and not description:
            continue
        result=predict_news(title,description)
        published_at=parse_datetime( article.get("publishedAt"))
        prediction= NewsPrediction.objects.create(
            title=title,
            text=description,
            source=(article.get("source")or {}).get("name",""),
            url=article.get("url",""),
            published_at=published_at,
            prediction=result["prediction"],
            label=result["label"],
        )
        saved_predictions.append(prediction)
    return saved_predictions