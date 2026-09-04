import os
import requests
from dotenv import load_dotenv
from django.utils.dateparse import parse_datetime
from detector.inference.predict import predict_news
from detector.models import NewsPrediction

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_SEARCH_URL = "https://newsapi.org/v2/everything"


def fetch_news(country="us", page_size=10,
               category=None, search=None):
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
    if category:
        params["category"] = category
    if search:
        params["q"] = search

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
    predictions = []

    for article in articles:
        url = (article.get("url") or "").strip()

        if not url:
            continue

        title = (article.get("title") or "").strip()
        description = (article.get("description") or "").strip()
        image_url = (article.get("urlToImage") or "").strip()

        if not title and not description:
            continue

        existing_prediction = NewsPrediction.objects.filter(
            url=url
        ).first()

        if existing_prediction:
            if image_url and existing_prediction.image_url!=image_url:
                existing_prediction.image_url = image_url
                existing_prediction.save(update_fields=["image_url"])
            predictions.append(existing_prediction)
            continue

        result = predict_news(title, description)

        published_at = parse_datetime(
            article.get("publishedAt") or ""
        )

        new_prediction = NewsPrediction.objects.create(
            title=title,
            text=description,
            source=(article.get("source") or {}).get("name", ""),
            url=url,
            image_url=image_url,
            published_at=published_at,
            prediction=result["prediction"],
            label=result["label"],
        )

        predictions.append(new_prediction)

    return predictions

def search_related_news(query, page_size=5):
    """
    Search for news articles related to a specific query using NewsAPI.
    """

    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not configured.")
    query = query.strip()
    if not query:
        raise ValueError("A search query is required.")

    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": page_size,
    }

    response = requests.get(
        NEWS_SEARCH_URL,
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