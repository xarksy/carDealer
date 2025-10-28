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


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role in ["admin"]):
            return view_func(request, *args, **kwargs)
        # return HttpResponseForbidden("Not allowed")
        return redirect("carList")

    return wrapper


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

def demo_api_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    cars = Cars.objects.all()
    return render(request, "demo/base1.html", {"cars": cars})

def demo_carlist_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    cars = Cars.objects.all()
    return render(request, "demo/api_dashboard.html", {"cars": cars})

@admin_required
def dashboard_customer_list(request):
    context = {
        'orders' : Order.objects.select_related("customer","trade_in_car").all()
    }

    return render(request,'cars/dashboard/customer_list.html',context)

def demo_logout(request):
    logout(request)
    return redirect("demo_login")
