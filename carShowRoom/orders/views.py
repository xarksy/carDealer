from django.shortcuts import render, redirect
from .models import Order
from customer.models import Customer
from .forms import OrderForm
from customer.forms import CustomerForm

# Create your views here.
def placing_order_view(request):
    action = request.GET.get("action",None)
    order_form, customer_form = None, None

    if request.method == "POST":
        if action == "Trade":
            order_form = OrderForm(request.POST)
            customer_form = CustomerForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():
                customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.offer_type = "trade"
                order.save()
                return redirect('detail')        
        elif action == "Buy":
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                pass

    return render(request,'orders/order_form.html', )