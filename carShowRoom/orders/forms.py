from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "offered_vehicle_model",
            "offered_vehicle_varian",
            "offered_vehicle_transmission",
            "offered_vehicle_province",
            "offered_vehicle_year",
            "offered_vehicle_kilometers",
            "offered_vehicle_notes",
        ]