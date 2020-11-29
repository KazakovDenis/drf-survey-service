from django.urls import path

from . import views


urlpatterns = [
    path('', views.SurveyListAPIView.as_view(), name='survey-list'),
    path('<uuid:pk>/', views.SurveyDetailAPIView.as_view(), name='survey-detail'),
]
