from django import forms
from .models import TradeInCar

class TradeinForm(forms.ModelForm):
    class Meta:
        model = TradeInCar
        fields = [
            "offered_vehicle_model",
            "offered_vehicle_varian",
            "offered_vehicle_transmission",
            "offered_vehicle_province",
            "offered_vehicle_year",
            "offered_vehicle_kilometers",
            "offered_vehicle_notes",
        ]