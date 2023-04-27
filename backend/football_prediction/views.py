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
FORMATION_REFERENCES_PATH = os.path.join(ML_PATH, "data/formations.json")
TEAM_REFERENCES_PATH = os.path.join(ML_PATH, "data/teams.json")
PLAYER_REFERENCES_PATH = os.path.join(ML_PATH, "data/player_references.csv")

df = pd.read_csv(PLAYER_REFERENCES_PATH, index_col=0).groupby(["player"], as_index=False).sum()
team_choices = json.load(open(TEAM_REFERENCES_PATH, mode='rb'))["teams"]
position_choices = json.load(open(FEATURES_PATH, mode='rb'))["position_choices"]
formation_choices = json.load(open(FORMATION_REFERENCES_PATH, mode='rb'))["formations"]


def index(request):
    return render(request, "football_prediction/index.html")


@api_view(["POST"])
def show_prediction(request):
    
    serializer = PredictionSerializer(data=request.data)
    print(request.data)
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

    serializer = PredictionSerializer(data=request.data)
    if serializer.is_valid():
        instance, players_not_found = create_instance(request.data)
        if len(players_not_found) > 0:
            return Response({
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
        return Response({
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
def get_available_players_by_team(request):
    # Error : (Caglar Soyuncu, Leicester)
    return JsonResponse(team_choices, safe=False)
    
    
@api_view(["GET"])
def get_available_positions(request):
    return JsonResponse(position_choices, safe=False)


@api_view(["GET"])
def get_available_positions_by_formation(request):
    return JsonResponse(formation_choices, safe=False)