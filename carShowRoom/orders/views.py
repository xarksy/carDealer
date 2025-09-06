from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from cars.models import Cars
from customer.models import Customer
from .forms import TradeinForm
from customer.forms import CustomerForm

# Create your views here.
def placing_order_view(request):
    action = request.GET.get("action",None)
    car_id = request.GET.get("car_id") or request.POST.get("car_id")
    car = get_object_or_404(Cars, id=car_id) if car_id else None

    order_form, customer_form = None, None

    if request.method == "POST":
        if action == "Trade":
            order_form = TradeinForm(request.POST)
            customer_form = CustomerForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():                
                customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.showroom_car = car
                order.offer_type = "trade"
                order.save()
                return redirect('detail_car')        
        elif action == "Buy":
            customer_form = CustomerForm(request.POST)
            order_form = TradeinForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():
                customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.showroom_car = car
                order.offer_type = "buy"
                order.save()
                return redirect('detail_car') 
    
    else:
        customer_form = CustomerForm()
        order_form = TradeinForm()

    context = {
        "customer_form": customer_form,
        "order_form": order_form,
        "action": action,
        "car_id": car_id
    }

    return render(request,'orders/order_form.html', context)