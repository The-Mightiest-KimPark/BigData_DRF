from django.urls import path, include
from . import views

urlpatterns = [
    path('api/answer-count/', views.AnswerCountGet),
    path('api/answer-save/', views.SaveCountGet)
]