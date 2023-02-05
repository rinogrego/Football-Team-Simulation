from django.db import models

# Create your models here.
# class User():
#     pass


class Prediction(models.Model):
    # identity and request date
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    datetime = models.DateTimeField(auto_now_add=True)
    
    # home players
    home_player_01 = models.CharField(max_length=40, null=False, blank=False)
    home_player_01_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_02 = models.CharField(max_length=40, null=False, blank=False)
    home_player_02_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_03 = models.CharField(max_length=40, null=False, blank=False)
    home_player_03_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_04 = models.CharField(max_length=40, null=False, blank=False)
    home_player_04_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_05 = models.CharField(max_length=40, null=False, blank=False)
    home_player_05_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_06 = models.CharField(max_length=40, null=False, blank=False)
    home_player_06_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_07 = models.CharField(max_length=40, null=False, blank=False)
    home_player_07_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_08 = models.CharField(max_length=40, null=False, blank=False)
    home_player_08_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_09 = models.CharField(max_length=40, null=False, blank=False)
    home_player_09_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_10 = models.CharField(max_length=40, null=False, blank=False)
    home_player_10_position = models.CharField(max_length=16, null=False, blank=False)
    home_player_11 = models.CharField(max_length=40, null=False, blank=False)
    home_player_11_position = models.CharField(max_length=16, null=False, blank=False)
    
    # away players
    away_player_01 = models.CharField(max_length=40, null=False, blank=False)
    away_player_01_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_02 = models.CharField(max_length=40, null=False, blank=False)
    away_player_02_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_03 = models.CharField(max_length=40, null=False, blank=False)
    away_player_03_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_04 = models.CharField(max_length=40, null=False, blank=False)
    away_player_04_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_05 = models.CharField(max_length=40, null=False, blank=False)
    away_player_05_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_06 = models.CharField(max_length=40, null=False, blank=False)
    away_player_06_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_07 = models.CharField(max_length=40, null=False, blank=False)
    away_player_07_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_08 = models.CharField(max_length=40, null=False, blank=False)
    away_player_08_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_09 = models.CharField(max_length=40, null=False, blank=False)
    away_player_09_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_10 = models.CharField(max_length=40, null=False, blank=False)
    away_player_10_position = models.CharField(max_length=16, null=False, blank=False)
    away_player_11 = models.CharField(max_length=40, null=False, blank=False)
    away_player_11_position = models.CharField(max_length=16, null=False, blank=False)
    
    # for predictions
    home_score_pred = models.FloatField(null=True, blank=False, default=-1) # default -1 indicating no prediction made
    away_score_pred = models.FloatField(null=True, blank=False, default=-1)
    LEVEL_CHOICES = (
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Lose'),
        ('None', 'None'), # None value indicating no prediction made
    )
    home_result_pred = models.CharField(max_length=4, choices=LEVEL_CHOICES, null=True, blank=False)
    
    def __str__(self) -> str:
        return 'name predict something'