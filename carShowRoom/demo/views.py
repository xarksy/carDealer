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
from django.core.paginator import Paginator

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
        
    return render(request, "demo/demo_login.html")

def demo_logout(request):
    logout(request)
    return redirect("demo_login")


# ========================= > Dashboard

def dashboard_of_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")
        
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
    

    return render(request, 'demo/chart_dashboard.html', context=context)


def demo_carlist_dashboard(request):
    # 1. Cek keamanan: Pastikan user sudah login
    if not request.user.is_authenticated:
        return redirect("demo_login")

    # 2. Ambil data mobil
    # Kita tambahkan .order_by('-id') agar data terbaru muncul paling atas.
    # Paginator membutuhkan data yang urutannya konsisten agar tidak error.
    cars_data = Cars.objects.all().order_by('-id')

    # 3. Logika "Items Per Page" (Jumlah data per halaman)
    # Kita cek apakah user memilih angka view dari dropdown (misal: 10, 25, 50)
    # Jika tidak ada yang dipilih, default-nya adalah 5 data per halaman.
    items_per_page = request.GET.get('paginate_by', 5)

    # Validasi: Pastikan items_per_page adalah angka. Jika error, kembalikan ke 5.
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 5

    # 4. Masukkan data ke Paginator
    paginator = Paginator(cars_data, items_per_page)

    # 5. Ambil nomor halaman yang sedang aktif dari URL (misal: ?page=2)
    page_number = request.GET.get('page')
    
    # Ambil objek halaman yang sesuai (Django otomatis menangani jika page kosong/invalid)
    page_obj = paginator.get_page(page_number)

    # 6. Siapkan data untuk dikirim ke HTML
    context = {
        "cars": page_obj,          # Data mobil yang sudah dipotong per halaman
        "items_per_page": items_per_page # Agar dropdown view tetap ingat pilihan terakhir user
    }

    return render(request, "demo/car_list_dashboard.html", context)

def dashboard_customer_list(request):
    context = {
        'orders' : Order.objects.select_related("customer","trade_in_car").all()
    }

    return render(request,'demo/customer_list_dashboard.html',context)
    # return render(request,'demo/api_demo_dashboard.html',context)


# ==================> Demo API
def demo_api(request):

    return render(request,'demo/api/demo_api.html')