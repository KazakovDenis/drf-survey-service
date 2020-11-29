from django.urls import path

from . import views


urlpatterns = [
    path('', views.SurveyListAPIView.as_view(), name='scheme-list'),
    path('<uuid:pk>/', views.SurveyResultAPIView.as_view(), name='take-survey'),
    path('<uuid:pk>/edit', views.SurveyDetailAPIView.as_view(), name='scheme-detail'),
]
