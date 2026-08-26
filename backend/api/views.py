from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from detector.inference.predict import predict_news
from detector.models import NewsPrediction

# Create your views here.
@api_view(["POST"])
def predict_news_api(request):
    title=request.data.get("title","")
    text=request.data.get("text","")

    if not title and not text:
        return Response(
            {"error":"title or text is required."},
            status=status.HTTP-400-BAD_REQUEST
        )
    try:
        result=predict_news(title,text)
        NewsPrediction.objects.create(
            title=title,
            text=text,
            prediction=result["prediction"],
            label=result["label"]
        )
        return Response(result,status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
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
        return Response(data,status=status.HTTP_200_OK)
