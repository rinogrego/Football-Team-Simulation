from django.shortcuts import render
from .models import Prediction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PredictionSerializer

import numpy as np
import pandas as pd
import os
import json

from .utils import create_instance, get_inference


ML_PATH = os.path.join(settings.BASE_DIR, "ml_stuffs")
FEATURES_PATH = os.path.join(ML_PATH, "models/baseline-feature.json")
PLAYER_REFERENCES_PATH = os.path.join(ML_PATH, "data/player_references.csv")

position_choices = json.load(open(FEATURES_PATH))["position_choices"]
df = pd.read_csv(PLAYER_REFERENCES_PATH, index_col=0).groupby(["player"], as_index=False).sum()


def index(request):
    # ref: https://stackoverflow.com/questions/62764900/check-if-the-user-has-logged-in-with-social-account-django
    # ref: https://ilovedjango.com/django/authentication/allauth/allauth-django/
    # ref: https://stackoverflow.com/questions/13139543/django-allauth-accessing-socialaccount-set-all-from-within-a-view
        
    return render(request, "football_prediction/index.html", context={
        # "message": message
    })


@api_view(["POST"])
def show_prediction(request):
    
    serializer = PredictionSerializer(data=request.data)
    if serializer.is_valid():
        instance, players_not_found = create_instance(request.data)
        if len(players_not_found) > 0:
            return JsonResponse({
                "message": "the following players you asked were not found in the database. since the player list came from the server then the error came from our part",
                "players_not_found": players_not_found
            })
            
        home_score, away_score, home_result = get_inference(instance)
        
        serializer.save(
            home_score_pred = home_score,
            away_score_pred = away_score,
            home_result_pred = home_result
        )
    else:
        return HttpResponseRedirect(reverse("index", args=[]))
    
    home_players = [value for key, value in serializer.data.items() if ("home" in key and "position" not in key)]
    home_positions = [value for key, value in serializer.data.items() if ("home" in key and "position" in key)]
    away_players = [value for key, value in serializer.data.items() if ("away" in key and "position" not in key)]
    away_positions = [value for key, value in serializer.data.items() if ("away" in key and "position" in key)]
    context = {
        "home_composition": [(name, pos) for name, pos in zip(home_players, home_positions)],
        "away_composition": [(name, pos) for name, pos in zip(away_players, away_positions)],
        "home_score_pred": serializer.data["home_score_pred"],
        "away_score_pred": serializer.data["away_score_pred"],
        "home_result_pred": serializer.data["home_result_pred"]
    }
    return render(request, "football_prediction/prediction.html", context=context)


@api_view(["POST"])
def predict(request):
    # ref: https://www.django-rest-framework.org/api-guide/serializers/
    # ref: https://stackoverflow.com/questions/38909652/using-curl-and-django-rest-framework-in-terminal
    # ref: https://devqa.io/curl-sending-api-requests/
    
    
    serializer = PredictionSerializer(data=request.data)
    if serializer.is_valid():
        instance, players_not_found = create_instance(request.data)
        if len(players_not_found) > 0:
            return JsonResponse({
                "message": "the following players you asked were not found in the database if you used the player list from the server then the error came from our part",
                "players_not_found": players_not_found
            })
            
        home_score, away_score, home_result = get_inference(instance)
        
        serializer.save(
            home_score_pred = home_score,
            away_score_pred = away_score,
            home_result_pred = home_result
        )
    else:
        return JsonResponse({
            "message": "djangorestframework serializer not valid. your input is probably missing."
        })
    
    return Response(serializer.data)


@api_view(["GET"])
def view_predictions(request):
    preds = Prediction.objects.all()
    serializer = PredictionSerializer(preds, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_available_players(request):
    players = np.sort(df.player.values).tolist()
    return JsonResponse(players, safe=False)


@api_view(["GET"])
def get_available_positions(request):
    return JsonResponse(position_choices, safe=False)