from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars
from .forms import CarsForm, ServiceHistoryForm
from django.http import HttpResponseForbidden
from customer.forms import CustomerForm
from orders.forms import TradeinForm
from orders.models import Order
from customer.models import Customer
from django.db.models import Sum, Count

import logging
logger = logging.getLogger(__name__)


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role in ["admin"]):
            return view_func(request, *args, **kwargs)
        # return HttpResponseForbidden("Not allowed")
        return redirect("carList")

    return wrapper

def carList(request):
    print(request.user)

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST or None)
        trade_form = TradeinForm(request.POST or None)

        if customer_form.is_valid() and trade_form.is_valid():
            customer = customer_form.save()
            order = Order(customer=customer, offer_type="sell") 
            placing_order = trade_form.save(commit=False)
            placing_order.customer = customer
            placing_order.save()
            order.trade_in_car = placing_order
            
            order.save()
            return redirect('success_page')
        else:
            logger.error("Form submission failed with errors: %s", {"customer_form": customer_form.errors, "trade_form": trade_form.errors})

    else:
        customer_form = CustomerForm()
        trade_form = TradeinForm()

    context = {
        'cars' : Cars.objects.all(),
        "customer_form": customer_form,
        "trade_form": trade_form,
    }

    return render(request,'cars/index.html',context)



# ====================== CRUD CAR
@admin_required
def create_car(request):

    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            next_url = request.GET.get('next', 'carList')
            return redirect(next_url)
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CarsForm()
    
    context = {
        'form': form
    }

    return render(request,'cars/car_form.html',context)


@admin_required
def updateCar(request, car_id):
    """
    View to update the details of a specific car.
    """
    car = get_object_or_404(Cars, id=car_id)
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()

            next_url = request.GET.get('next', 'carList')
            return redirect(next_url)
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CarsForm(instance=car)
    
    context = {
        'form': form
    }

    return render(request, 'cars/car_form.html',context=context)

@admin_required
def deleteCar(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    car.delete()

    # return redirect('carList')
    next_url = request.GET.get('next', 'carList')
    return redirect(next_url)

def detail_car(request, car_id):

    car = get_object_or_404(Cars, id=car_id)
    service_history = car.service_histories.all()
    total_biaya = sum(service.biaya for service in service_history)    

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save()
            order = Order(customer=customer, offer_type="buy")
            order.showroom_car = car
            order.save()
            # form.save()
            return redirect('carList')
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CustomerForm()

    context = {
        'car': car,
        'service_history': service_history,
        'total_biaya': total_biaya,
        'cash': total_biaya + car.harga,
        'trade_in_forms': form
    }

    return render(request, 'cars/detail.html', context)

# ===== CRUD CAR SERVICE
@admin_required
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

@admin_required
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


#===============================  Dashboard view
@admin_required
def dashboard_car_list(request):

    context = {
        'cars' : Cars.objects.all()
    }

    return render(request,'cars/dashboard/car_list.html',context)

@admin_required
def dashboard_customer_list(request):
    context = {
        'orders' : Order.objects.select_related("customer","trade_in_car").all()
    }

    return render(request,'cars/dashboard/customer_list.html',context)

@admin_required
def dashboard_of_dashboard(request):    
    total_order = Order.objects.count()
    total_customers = Customer.objects.count()
    total_cars = Cars.objects.count()

    total_income = Order.objects.aggregate(total=Sum("showroom_car__harga"))["total"] or 0
    order_per_month = (
        Order.objects.values("created_at__month")
        .annotate(total=Count("id"))
        .order_by("created_at__month")
    )

    context = {
        'total_order' : total_order,
        'total_customer' : total_customers,
        'total_cars' : total_cars,
        'total_income' : total_income,
        'order_per_month' : order_per_month,
    }
    

    return render(request, 'cars/dashboard/dashboard.html', context=context)

#=============== success page
def success_page(request):

    return render(request, 'cars/success_page.html')