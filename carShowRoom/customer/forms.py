from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # exclude = ['customer_type']
        fields = ['name','phone_number','email','address']