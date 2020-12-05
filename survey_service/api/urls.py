from django.urls import include, path
from rest_framework.authtoken import views

from .views import api_versions_list


urlpatterns = [
    path('', api_versions_list, name='api-versions-list'),
    path('auth/', include('rest_framework.urls')),
    path('auth/get-token/', views.obtain_auth_token, name='get-token'),
    path('v1/', include('api.v1.urls')),
]
