from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from detector.inference.predict import predict_news

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
        return Response(result,status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

