from django.shortcuts import render
from .models import User, Prediction

# Create your views here.
def index(request):
    # ref: https://stackoverflow.com/questions/62764900/check-if-the-user-has-logged-in-with-social-account-django
    # ref: https://ilovedjango.com/django/authentication/allauth/allauth-django/
    # ref: https://stackoverflow.com/questions/13139543/django-allauth-accessing-socialaccount-set-all-from-within-a-view
    return render(request, "index.html")

def predict(request):
    # check user is authenticated or not
    #request.user.is_authenticated()
    if request.method == "POST":
        
        _pred_request_kwargs = {}
        _pred_request_kwargs["user"] = request.user.username
        for team in ['home', 'away']:
            for i in range(1, 11):
                _player_string = team+"_player_"+f"{i}".zfill(2)
                _pred_request_kwargs[_player_string] = request.POST.get(_player_string)
            
        pred_request = Prediction(**_pred_request_kwargs)
        pred_request.save()
        pred_request_id = pred_request.id
        
        
        # home players
        home_player_01 = request.POST.get('home_player_01')
        home_player_02 = request.POST.get('home_player_02')
        home_player_03 = request.POST.get('home_player_03')
        home_player_04 = request.POST.get('home_player_04')
        home_player_05 = request.POST.get('home_player_05')
        home_player_06 = request.POST.get('home_player_06')
        home_player_07 = request.POST.get('home_player_07')
        home_player_08 = request.POST.get('home_player_08')
        home_player_09 = request.POST.get('home_player_09')
        home_player_10 = request.POST.get('home_player_10')
        home_player_11 = request.POST.get('home_player_11')
        
        # away players
        away_player_01 = request.POST.get('away_player_01')
        away_player_02 = request.POST.get('away_player_02')
        away_player_03 = request.POST.get('away_player_03')
        away_player_04 = request.POST.get('away_player_04')
        away_player_05 = request.POST.get('away_player_05')
        away_player_06 = request.POST.get('away_player_06')
        away_player_07 = request.POST.get('away_player_07')
        away_player_08 = request.POST.get('away_player_08')
        away_player_09 = request.POST.get('away_player_09')
        away_player_10 = request.POST.get('away_player_10')
        away_player_11 = request.POST.get('away_player_11')
        
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