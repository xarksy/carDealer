from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        field = ['name','phone_number','email','address','customer_type','status','notes','merek','model','tahun','transmisi','varian','provinsi','kilometer']