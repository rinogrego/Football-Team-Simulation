from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
  # path("", include('router.urls')),
  # path("api/", include('rest_framework.urls', namespace='rest_framework')),
  path("", views.index, name="index"),
  path("predict", views.show_prediction, name="show-prediction"),
  
  # api
  path("api/predict/", views.predict, name="predict"),
  path("api/view-predictions/", views.view_predictions, name="view-predict"),
  path("api/database/players/", views.get_available_players, name="get-players"),
  path("api/database/teams/", views.get_available_players_by_team, name="get-teams"),
  path("api/database/positions/", views.get_available_positions, name="get-positions"),
  path("api/database/formations/", views.get_available_positions_by_formation, name="get-formations")
]