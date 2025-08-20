from django.shortcuts import render, redirect, get_object_or_404
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

def detail_car(request, car_id):

    car = get_object_or_404(Cars, id=car_id)
    service_history = car.service_histories.all()
    total_biaya = sum(service.biaya for service in service_history)
    context = {
        'car': car,
        'service_history': service_history,
        'total_biaya': total_biaya,
        'cash': total_biaya + car.harga
    }
    return render(request, 'cars/detail.html', context)

def updateCar(request, car_id):
    """
    View to update the details of a specific car.
    """
    car = get_object_or_404(Cars, id=car_id)
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('carList')
    else:
        form = CarsForm(instance=car)
    
    context = {
        'form': form
    }

    return render(request, 'cars/car_form.html',context=context)

def deleteCar(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    car.delete()

    return redirect('carList')

def car_service_plain(request):
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carList')
    else:
        form = ServiceHistoryForm()
    
    context = {
        'form' : form
    }

    return render(request, 'cars/service_history_form.html', context)

def car_service(request, car_id):
    car = get_object_or_404(Cars, car_id)
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST, request.FILES, hide_car_field=True)
        if form.is_valid():
            service_history = form.save(commit=False)
            service_history.car = car
            service_history.save()
            return redirect('detail_car',car_id=car.id)
    else:
        form = ServiceHistoryForm(initial={'mobil': car.id}, hide_car_field=True)
    
    context = {
        'form' : form,
        'car' : car,
    }

    return redirect(request,'cars/service_history_form.html', context)