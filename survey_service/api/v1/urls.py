from django.urls import include, path

from rest_framework import routers

from .views import UserViewSet, SurveyViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('surveys', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
