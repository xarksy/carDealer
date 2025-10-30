from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from cars.models import Cars
from cars.forms import CarsForm, ServiceHistoryForm
from django.http import HttpResponseForbidden
from customer.forms import CustomerForm
from orders.forms import TradeinForm
from orders.models import Order
from customer.models import Customer
from django.db.models import Sum, Count

import logging
logger = logging.getLogger(__name__)

User = get_user_model()


def demo_login(request):
    if request.method == "POST":
        role = request.POST.get("role")
        creds = {
            "admin": ("admin_demo", "admin123"),
            "sales": ("sales_demo", "sales123"),
            "customer": ("customer_demo", "customer123"),
        }
        username, password = creds.get(role, (None, None))
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("demo_dashboard")
        
    return render(request, "demo/api_login.html")

def demo_logout(request):
    logout(request)
    return redirect("demo_login")

def demo_api_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    cars = Cars.objects.all()
    return render(request, "demo/base1.html", {"cars": cars})

# ========================= > Dashboard

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
    

    return render(request, 'demo/demo_dashboard.html', context=context)


def demo_carlist_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    cars = Cars.objects.all()
    return render(request, "demo/api_dashboard.html", {"cars": cars})

def dashboard_customer_list(request):
    context = {
        'orders' : Order.objects.select_related("customer","trade_in_car").all()
    }

    return render(request,'demo/customer_list_dashboard.html',context)


