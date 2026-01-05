from django import forms
from .models import Cars, ServiceHistory
from django.core.exceptions import ValidationError

class CarsForm(forms.ModelForm):
    """
    Form for creating and updating Cars instances.
    """
    # Field tambahan untuk upload banyak gambar (tidak masuk langsung ke model Cars)
    # gallery_images = forms.FileField(
    #     required=False,
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #     label="Foto Galeri Tambahan"
    # )

    class Meta:
        model = Cars
        fields = ['nama', 'harga', 'status', 'merek', 'model', 'tahun', 'kilometer', 'transmisi', 'jenis_bahan_bakar', 'mesin', 'tempat_duduk', 'deskripsi','gambar']
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
 
class ServiceHistoryForm (forms.ModelForm):
    def __init__(self, *args, hide_car_field=False, **kwargs):
        super().__init__(*args, **kwargs)
        if hide_car_field:
            self.fields['mobil'].widget = forms.HiddenInput()
    """
    Form for creating and updating ServiceHistory instances.
    """
    class Meta:
        model = ServiceHistory
        fields = ['mobil', 'tanggal_service', 'deskripsi', 'biaya']
        widgets = {
            'tanggal_service': forms.DateInput(attrs={'type': 'date'}),
        }