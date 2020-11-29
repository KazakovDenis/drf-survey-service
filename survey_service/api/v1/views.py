from django.shortcuts import redirect
from rest_framework import permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'admin': {
            'schemes': reverse('scheme-list', request=request, format=format),
            'participants': reverse('participant-list', request=request, format=format),
        },
        'participant': reverse('survey-list', request=request, format=format)
    })


class SchemeAPIViewMixin:
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class SchemeListAPIView(SchemeAPIViewMixin, generics.ListCreateAPIView):
    """API endpoint для просмотра и редактирования списка опросов"""


class SchemeDetailAPIView(SchemeAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для просмотра и редактирования конкретного опроса"""


# todo: read only
class SurveyAPIViewMixin:
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class SurveyListAPIView(SurveyAPIViewMixin, generics.ListAPIView):
    """API endpoint для просмотра списка опросов участником"""


class SurveyDetailAPIView(SurveyAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для заполнения опроса участником"""


# class SurveyListAPIView(APIView):
#     """API endpoint списка опросов для участника"""
#
#     def get(self, request, pk):
#         survey = get_object_or_404(Scheme, pk=pk)
#         serializer = SurveySerializer(survey, context={'request': request})
#         return Response({'survey': serializer.data})
#
#     def post(self, request, pk):
#         survey = get_object_or_404(Scheme, pk=pk)
#         serializer = SurveySerializer(survey, data=request.data)
#         if not serializer.is_valid():
#             return Response({'serializer': serializer.data})
#         serializer.save()
#         return redirect('survey-list')
#
#
# class SurveyDetailAPIView(APIView):
#     """API endpoint формы опроса для участника"""


class ParticipantAPIViewMixin:
    queryset = Participant.objects.all()
    serializer_class = ParticipantListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class ParticipantListAPIView(ParticipantAPIViewMixin, generics.ListAPIView):
    """API endpoint списка участников опроса"""


class ParticipantDetailAPIView(ParticipantAPIViewMixin, generics.RetrieveUpdateAPIView):
    """API endpoint информации об участнике опроса"""
