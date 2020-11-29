from django.shortcuts import redirect
from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class SurveyListAPIView(generics.ListCreateAPIView):
    """API endpoint для просмотра и редактирования списка опросов"""
    queryset = Scheme.objects.all()
    serializer_class = SurveyListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class SurveyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для просмотра и редактирования конкретного опроса"""
    queryset = Scheme.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class SurveyResultAPIView(APIView):
    """API endpoint формы опроса для участника"""

    def get(self, request, pk):
        survey = get_object_or_404(Scheme, pk=pk)
        serializer = SurveySerializer(survey, context={'request': request})
        return Response({'survey': serializer.data})

    def post(self, request, pk):
        survey = get_object_or_404(Scheme, pk=pk)
        serializer = SurveySerializer(survey, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer.data})
        serializer.save()
        return redirect('survey-list')
