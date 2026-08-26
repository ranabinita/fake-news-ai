from django.urls import path
from . import views

urlpatterns=[
    path("predict/",views.predict_news_api,name="predict-news"),
]