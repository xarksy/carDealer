from django.shortcuts import render
from .models import Cars
from .forms import CarsForm, ServiceHistoryForm

# Create your views here.
def carList(request):

    context = {
        'cars' : Cars.objects.all()
    }

    return render(request,'cars/index.html',context)

def create_car(request):

    return render()