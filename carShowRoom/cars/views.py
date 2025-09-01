from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars
from .forms import CarsForm, ServiceHistoryForm
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)


def admin_or_sales_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role in ["admin","salesperson"]):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Not allowed")
    return wrapper


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('carList')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'cars/login_form.html')

def logout_view(request):
    logout(request)
    return redirect("login")

# Create your views here.
def carList(request):

    context = {
        'cars' : Cars.objects.all()
    }

    return render(request,'cars/index.html',context)

@admin_or_sales_required
def create_car(request):

    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carList')
        else:
            logger.error("Form submission failed: %s", form.errors)
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
            logger.error("Form submission failed: %s", form.errors)
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

    return render(request, 'cars/service_history_form.html', context=context)

def car_service(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
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
        'car' : car
    }

    return render(request,'cars/service_history_form.html', context=context)

