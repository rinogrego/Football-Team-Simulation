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
def _predict(request):
    # check user is authenticated or not
    #request.user.is_authenticated()
    if request.method == "POST":
        
        _pred_request_kwargs = {}
        _pred_request_kwargs["user"] = request.user.username
        for team in ['home', 'away']:
            for i in range(1, 11):
                _player_string = team+"_player_"+f"{i}".zfill(2)
                _pred_request_kwargs[_player_string] = request.POST.get(_player_string)
                _pred_request_kwargs[_player_string+"_position"] = request.POST.get(_player_string+"_position")
            
        pred_request = Prediction(**_pred_request_kwargs)
        pred_request.save()
        pred_request_id = pred_request.id
        
        
        # home players
        home_player_01 = request.POST.get('home_player_01')
        home_player_01_position = request.POST.get('home_player_01_position')
        home_player_02 = request.POST.get('home_player_02')
        home_player_02_position = request.POST.get('home_player_02_position')
        home_player_03 = request.POST.get('home_player_03')
        home_player_03_position = request.POST.get('home_player_03_position')
        home_player_04 = request.POST.get('home_player_04')
        home_player_04_position = request.POST.get('home_player_04_position')
        home_player_05 = request.POST.get('home_player_05')
        home_player_05_position = request.POST.get('home_player_05_position')
        home_player_06 = request.POST.get('home_player_06')
        home_player_06_position = request.POST.get('home_player_06_position')
        home_player_07 = request.POST.get('home_player_07')
        home_player_07_position = request.POST.get('home_player_07_position')
        home_player_08 = request.POST.get('home_player_08')
        home_player_08_position = request.POST.get('home_player_08_position')
        home_player_09 = request.POST.get('home_player_09')
        home_player_09_position = request.POST.get('home_player_09_position')
        home_player_10 = request.POST.get('home_player_10')
        home_player_10_position = request.POST.get('home_player_10_position')
        home_player_11 = request.POST.get('home_player_11')
        home_player_11_position = request.POST.get('home_player_11_position')
        
        # away players
        away_player_01 = request.POST.get('away_player_01')
        away_player_01_position = request.POST.get('away_player_01_position')
        away_player_02 = request.POST.get('away_player_02')
        away_player_02_position = request.POST.get('away_player_02_position')
        away_player_03 = request.POST.get('away_player_03')
        away_player_03_position = request.POST.get('away_player_03_position')
        away_player_04 = request.POST.get('away_player_04')
        away_player_04_position = request.POST.get('away_player_04_position')
        away_player_05 = request.POST.get('away_player_05')
        away_player_05_position = request.POST.get('away_player_05_position')
        away_player_06 = request.POST.get('away_player_06')
        away_player_06_position = request.POST.get('away_player_06_position')
        away_player_07 = request.POST.get('away_player_07')
        away_player_07_position = request.POST.get('away_player_07_position')
        away_player_08 = request.POST.get('away_player_08')
        away_player_08_position = request.POST.get('away_player_08_position')
        away_player_09 = request.POST.get('away_player_09')
        away_player_09_position = request.POST.get('away_player_09_position')
        away_player_10 = request.POST.get('away_player_10')
        away_player_10_position = request.POST.get('away_player_10_position')
        away_player_11 = request.POST.get('away_player_11')
        away_player_11_position = request.POST.get('away_player_11_position')
        
        # save prediction attempt to database
        # pred_request = Prediction(
        #     user = request.user.username-or-something
            
        #     home_player_01 = home_player_01,
        #     home_player_02 = home_player_02,
        #     home_player_03 = home_player_03,
        #     home_player_04 = home_player_04,
        #     home_player_05 = home_player_05,
        #     home_player_06 = home_player_06,
        #     home_player_07 = home_player_07,
        #     home_player_08 = home_player_08,
        #     home_player_09 = home_player_09,
        #     home_player_10 = home_player_10,
        #     home_player_11 = home_player_11,
            
        #     away_player_01 = away_player_01,
        #     away_player_02 = away_player_02,
        #     away_player_03 = away_player_03,
        #     away_player_04 = away_player_04,
        #     away_player_05 = away_player_05,
        #     away_player_06 = away_player_06,
        #     away_player_07 = away_player_07,
        #     away_player_08 = away_player_08,
        #     away_player_09 = away_player_09,
        #     away_player_10 = away_player_10,
        #     away_player_11 = away_player_11,
        # )
        # pred_request.save()
        
        # get attributes & construct dataframes
        #process home players
        #process away players
        
        # construct inputs dataframe
        #pd.concat
        
        # predict
        #model = load_model()
        #preds = model.predict
        #home_score_pred = 
        #away_score_pred = 
        #home_result_pred =
        
        # save prediction result to database 
        #try:
        # pred_request.home_score_pred = home_score_pred
        # pred_request.away_score_pred = away_score_pred
        # pred_request.home_result_pred = home_result_pred
        # pred_request.save()
        #except:
        # return render(request, "...", {"err": "Error, cannot do prediction"}, status=500 #Internal server error)
        
    return render(request, "predict.html")


@api_view(["POST"])
def predict(request):
    # ref: https://www.django-rest-framework.org/api-guide/serializers/
    # ref: https://stackoverflow.com/questions/38909652/using-curl-and-django-rest-framework-in-terminal
    # ref: https://devqa.io/curl-sending-api-requests/
    
    instance = create_instance(request.data)
    preds = model.predict([instance])
    home_score = preds[0][0][0]
    away_score = preds[0][0][1]
    home_result = np.argmax(preds[1][0])
    home_result_dict = {0: "W", 1: "D", 2:"L"}
    home_result = home_result_dict[home_result]
    serializer = PredictionSerializer(data=request.data)
    
    if serializer.is_valid():
        print("prediction serializer is valid!")
        saved_serializer = serializer.save(
            home_score_pred = home_score,
            away_score_pred = away_score,
            home_result_pred = home_result
        )
        print("saved serializer")
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