from django.urls import path

from . import views


urlpatterns = [
    path('', views.api_v1_root, name='api-v1-root'),
    path('doc/', views.api_spec, name='api-v1-doc'),
    path('schemes/', views.SchemeListAPIView.as_view(), name='scheme-list'),
    path('schemes/<uuid:pk>', views.SchemeDetailAPIView.as_view(), name='scheme-detail'),
    path('schemes/<uuid:pk>/take', views.scheme_take, name='scheme-take'),
    path('surveys/', views.SurveyListAPIView.as_view(), name='survey-list'),
    path('surveys/<uuid:pk>', views.SurveyDetailAPIView.as_view(), name='survey-detail'),
    path('participants/', views.ParticipantListAPIView.as_view(), name='participant-list'),
    path('participants/<int:pk>', views.ParticipantDetailAPIView.as_view(), name='participant-detail'),
]
