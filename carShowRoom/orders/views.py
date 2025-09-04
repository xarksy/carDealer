from django.shortcuts import render
from .models import Order
from customer.models import Customer

# Create your views here.
def placing_order_view(request):

    return render(request,'orders/order_form.html')