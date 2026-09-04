from http.client import BAD_REQUEST

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from detector.inference.predict import predict_news
from detector.models import NewsPrediction
from detector.ingestion.fetch_news import (fetch_news,
                                           analyze_and_save_news,
                                           search_related_news,)


# Create your views here.
@api_view(["POST"])
def predict_news_api(request):
    title=request.data.get("title","").strip()
    text=request.data.get("text","").strip()

    if not title and not text:
        return Response(
            {"error":"title or text is required."},
            status=status.HTTP-400-BAD_REQUEST,
        )
    try:
        result=predict_news(title,text)
        if title:
            search_query=title
        else:
            search_query=" ".join(text.split()[:12])
        related_articles=[]
        search_error=""
        try:
            articles=search_related_news(
                query=search_query,
                page_size=5,
            )
            for article in articles:
                article_title=(
                    article.get("title") or ""
                ).strip()
                article_url=(
                    article.get("url") or ""
                ).strip()
                if not article_title or not article_url:
                    continue
                related_articles.append({
                    "title":article_title,
                    "description":(
                        article.get("description") or ""
                    ).strip(),
                    "source":(
                        article.get("source") or {}
                    ).get("name",""),
                    "url":article_url,
                    "image_url":(
                        article.get("urlToImage") or ""
                    ).strip(),
                    "published_at":article.get("publishedAt"),
                })
        except Exception as error:
            search_error=str(error)
        NewsPrediction.objects.create(
            title=title,
            text=text,
            prediction=result["prediction"],
            label=result["label"]
        )
        return Response({
            "prediction":result["prediction"],
            "label":result["label"],
            "search_query":search_query,
            "related_articles":related_articles,
            "related_count":len(related_articles),
            "search_error":search_error
        },status=status.HTTP_200_OK,)
    except Exception as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def prediction_history(request):
    predictions= NewsPrediction.objects.all().order_by("-created_at")
    data=[]
    for prediction in predictions:
        data.append({
            "id":prediction.id,
            "title":prediction.title,
            "text":prediction.text,
            "prediction":prediction.prediction,
            "label":prediction.label,
            "created_at":prediction.created_at,
        })
    return Response(data, status=status.HTTP_200_OK)
@api_view(["GET"])
def live_news(request):
    try:
        country = request.query_params.get("country", "us")
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        try:
            page_size = int(request.query_params.get("page_size", 10))
        except ValueError:
            return Response(
                {"error": "Invalid page_size parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        page_size = max(1, min(page_size, 100))  # Ensure page_size is between 1 and 100
        articles=fetch_news(
            country=country,
            page_size=page_size,
            category=category,
            search=search)
        predictions=analyze_and_save_news(articles)
        data=[]
        for prediction in predictions:
            data.append({
                "id":prediction.id,
                "title":prediction.title,
                'description':prediction.text,
                'source':prediction.source,
                'url':prediction.url,
                'image_url':prediction.image_url,
                'published_at':prediction.published_at,
                'prediction':prediction.prediction,
                'label':prediction.label,
            })
        return Response({
            'count':len(data),
            'results':data
        }, status=status.HTTP_200_OK,)
    except Exception as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
