from django.shortcuts import render
from .models import Order
from customer.models import Customer
from .forms import OrderForm
from customer.forms import CustomerForm

# Create your views here.
def placing_order_view(request):

    return render(request,'orders/order_form.html')