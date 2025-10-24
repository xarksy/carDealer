from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from cars.models import Cars
from django.contrib.auth import get_user_model

User = get_user_model()

def demo_api_login(request):
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
    return render(request, "demo/login.html")

def demo_api_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    cars = Cars.objects.all()
    return render(request, "demo/dashboard.html", {"cars": cars})

def demo_api_logout(request):
    logout(request)
    return redirect("demo_login")
