from rest_framework import permissions, viewsets

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class SurveyViewSet(viewsets.ModelViewSet):
    """API endpoint для просмотра и редактирования опросов"""
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
