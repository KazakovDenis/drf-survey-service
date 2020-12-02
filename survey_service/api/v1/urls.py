from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from . import views


doc_view = TemplateView.as_view(
    template_name='redoc.html',
    extra_context={'schema_url': 'openapi-schema'}
)

urlpatterns = [
    path('', views.api_v1_root, name='api-v1-root'),
    path('doc/', doc_view, name='api-v1-doc'),
    path('openapi/', get_schema_view(title='Survey service backend API',), name='openapi-schema'),
    path('schemes/', views.SchemeListAPIView.as_view(), name='scheme-list'),
    path('schemes/<uuid:pk>', views.SchemeDetailAPIView.as_view(), name='scheme-detail'),
    path('schemes/<uuid:pk>/take', views.scheme_take, name='scheme-take'),
    path('surveys/', views.SurveyListAPIView.as_view(), name='survey-list'),
    path('surveys/<uuid:pk>', views.SurveyDetailAPIView.as_view(), name='survey-detail'),
    path('participants/', views.ParticipantListAPIView.as_view(), name='participant-list'),
    path('participants/<int:pk>', views.ParticipantDetailAPIView.as_view(), name='participant-detail'),
]
