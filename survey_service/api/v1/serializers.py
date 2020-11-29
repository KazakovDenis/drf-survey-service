from django.contrib.auth.models import User
from rest_framework import serializers

from survey.models import Survey


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survey
        fields = ['url', 'id', 'name', 'description', 'date_from', 'date_to']
