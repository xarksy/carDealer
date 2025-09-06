from django.shortcuts import render, redirect
from .models import Order
from customer.models import Customer
from .forms import OrderForm
from customer.forms import CustomerForm

# Create your views here.
def placing_order_view(request):
    action = request.GET.get("action",None)
    car_id = request.GET.get("car_id") or request.POST.get("car_id")
    order_form, customer_form = None, None

    if request.method == "POST":
        if action == "Trade":
            order_form = OrderForm(request.POST)
            customer_form = CustomerForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():                
                customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.showroom_car = car_id
                order.offer_type = "trade"
                order.save()
                return redirect('detail')        
        elif action == "Buy":
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.showroom_car = car_id
                order.offer_type = "buy"
                order.save()
                return redirect('detail') 
    
    else:
        customer_form = CustomerForm()
        order_form = OrderForm()

    context = {
        "customer_form": customer_form,
        "order_form": order_form,
        "action": action,
        "car_id": car_id
    }

    return render(request,'orders/order_form.html', context)