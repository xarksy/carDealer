from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # exclude = ['customer_type']
        fields = ['name','phone_number','email','address']
    
    def save(self, commit=True):
        phone_number = self.cleaned_data.get('phone_number')
        name = self.cleaned_data.get('name')

        # Reuse existing customer or create a new one
        customer, created = Customer.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                'name': name,
                'email': self.cleaned_data.get('email'),
                'address': self.cleaned_data.get('address'),
            }
        )

        # If existing, update fields in case they changed
        if not created:
            customer.name = name
            customer.email = self.cleaned_data.get('email')
            customer.address = self.cleaned_data.get('address')
            if commit:
                customer.save()

        return customer