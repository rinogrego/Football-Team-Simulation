from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
  path("", include('router.urls')),
  path("api/", include('rest_framework.urls', namespace='rest_framework')),
]