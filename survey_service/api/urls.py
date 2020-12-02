from django.urls import include, path

from .views import api_versions_list


urlpatterns = [
    path('', api_versions_list, name='api-versions-list'),
    path('auth/', include('rest_framework.urls')),
    path('v1/', include('api.v1.urls')),
]
