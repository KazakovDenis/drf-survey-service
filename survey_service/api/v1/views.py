from rest_framework import permissions, generics

from .serializers import *


class SurveyListAPIView(generics.ListCreateAPIView):
    """API endpoint для просмотра и редактирования опросов"""
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer


class SurveyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
