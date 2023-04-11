from django.shortcuts import render
from .models import Prediction
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PredictionSerializer

from tensorflow import keras
import numpy as np
import pandas as pd

from .utils import create_instance

model = keras.models.load_model("models/baseline-model.h5")
print("model loaded")


def index(request):
    # ref: https://stackoverflow.com/questions/62764900/check-if-the-user-has-logged-in-with-social-account-django
    # ref: https://ilovedjango.com/django/authentication/allauth/allauth-django/
    # ref: https://stackoverflow.com/questions/13139543/django-allauth-accessing-socialaccount-set-all-from-within-a-view
    return render(request, "football_prediction/index.html")


@api_view(["POST"])
def predict(request):
    # ref: https://www.django-rest-framework.org/api-guide/serializers/
    # ref: https://stackoverflow.com/questions/38909652/using-curl-and-django-rest-framework-in-terminal
    # ref: https://devqa.io/curl-sending-api-requests/
    
    instance = create_instance(request.data)
    # for key, value in instance.items():
    #     print(key, value.shape)
    preds = model.predict([instance])
    home_score = preds[0][0][0]
    away_score = preds[0][0][1]
    home_result = np.argmax(preds[1][0])
    home_result_dict = {0: "W", 1: "D", 2:"L"}
    home_result = home_result_dict[home_result]
    serializer = PredictionSerializer(data=request.data)
    
    if serializer.is_valid():
        saved_serializer = serializer.save(
            home_score_pred = home_score,
            away_score_pred = away_score,
            home_result_pred = home_result
        )
    else:
        print("serializer not valid")
    
    return Response(serializer.data)


@api_view(["GET"])
def view_predictions(request):
    preds = Prediction.objects.all()
    serializer = PredictionSerializer(preds, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_available_players(request):
    df = pd.read_csv("data/transformed/player_references.csv", index_col=0)
    players = np.sort(df.player.values).tolist()
    return JsonResponse(players, safe=False)


@api_view(["GET"])
def get_available_positions(request):
    POSITION_CHOICES = [
        "GK", 
        "DF", "CB", "FB", "LB", "RB", "WB",
        "MF", "DM", "CM", "LM", "RM", "WM", "AM",
        "FW", "LW", "RW"
    ]
    return JsonResponse(POSITION_CHOICES, safe=False)