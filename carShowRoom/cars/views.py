from django.shortcuts import render, redirect
from .models import Cars
from .forms import CarsForm, ServiceHistoryForm

# Create your views here.
def carList(request):

    context = {
        'cars' : Cars.objects.all()
    }

    return render(request,'cars/index.html',context)

def create_car(request):

    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carList')
    else:
        form = CarsForm()
    
    context = {
        'form': form
    }

    return render(request,'cars/car_form.html',context)