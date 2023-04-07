from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
  # path("", include('router.urls')),
  # path("api/", include('rest_framework.urls', namespace='rest_framework')),
  path("", views.index, name="index"),
  path("api/predict/", views.predict, name="predict"),
  path("api/view-predictions/", views.view_predictions, name="view-predict"),
  # api/predict/
  path("api/database/players/", views.get_available_players, name="get-players"),
  path("api/database/positions/", views.get_available_positions, name="get-positions")
]