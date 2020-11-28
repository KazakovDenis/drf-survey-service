from django.contrib import admin
from django.urls import path

from .v1 import views


urlpatterns = [
    path('v1/', views),
]
