from django.contrib import admin

# Register your models here.
from .models import Prediction


class PredictionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Prediction._meta.get_fields()]
    

admin.site.register(Prediction, PredictionAdmin)