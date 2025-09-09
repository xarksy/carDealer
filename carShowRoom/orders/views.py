from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from cars.models import Cars
from customer.models import Customer
from .forms import TradeinForm
from customer.forms import CustomerForm

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def placing_order_view(request):
    action = request.GET.get("action",None)
    car_id = request.GET.get("car_id") or request.POST.get("car_id")
    car = get_object_or_404(Cars, id=car_id) if car_id else None
    id_nya = int(car_id.strip())
    # order_form, customer_form = None, None

    if request.method == "POST":
        trade_form = TradeinForm(request.POST or None)
        customer_form = CustomerForm(request.POST or None)
        if action == "Trade":            
            if trade_form.is_valid() and customer_form.is_valid():                
                customer = customer_form.save()
                order = Order(customer=customer, offer_type="trade") 
                placing_order = trade_form.save(commit=False)
                placing_order.customer = customer
                placing_order.save()
                order.trade_in_car = placing_order
                order.showroom_car = car
                order.save()
                return redirect('detail_car',car_id=id_nya)   
            else:
                logger.error("Form submission failed with errors: %s", {"customer_form": customer_form.errors, "trade_form": trade_form.errors})     
        elif action == "Buy":
            if trade_form.is_valid() and customer_form.is_valid():                
                customer = customer_form.save()
                order = Order(customer=customer, offer_type="buy")                 
                order.showroom_car = car
                order.save()
                return redirect('detail_car',car_id=id_nya)   

            else:
                logger.error("Form submission failed with errors: %s", {"customer_form": customer_form.errors, "order_form": trade_form.errors})
                
    else:
        customer_form = CustomerForm()
        trade_form = TradeinForm()

    context = {
        "customer_form": customer_form,
        "trade_form": trade_form,
        "action": action,
        "car_id": car_id
    }

    return render(request,'orders/order_form.html', context)