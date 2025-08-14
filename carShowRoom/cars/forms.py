from django import forms
from .models import Cars, ServiceHistory
from django.core.exceptions import ValidationError

class CarsForm(forms.ModelForm):
    """
    Form for creating and updating Cars instances.
    """
    class Meta:
        model = Cars
        fields = ['nama', 'harga', 'merek', 'model', 'tahun', 'kilometer', 'transmisi', 'jenis_bahan_bakar', 'mesin', 'tempat_duduk', 'deskripsi']
        # widgets = {
        #     'gambar': forms.ClearableFileInput(attrs={'multiple': True}),
        # }
        def clean_harga(self):
            """
            Validate the harga field to ensure it is a positive number.
            """
            harga = self.cleaned_data.get('harga')
            if harga <= 0:
                raise ValidationError("Harga harus lebih dari 0.")
            return harga
 
