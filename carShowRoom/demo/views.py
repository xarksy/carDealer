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
    if not request.user.is_authenticated:
        return redirect("demo_login")

    # 1. Mulai dengan mengambil SEMUA data
    cars_data = Cars.objects.all()

    # ================= LOGIKA FILTERING (PENYARINGAN) =================
    
    # Filter by Merek (Brand)
    selected_brand = request.GET.get('brand')
    if selected_brand and selected_brand != "":
        cars_data = cars_data.filter(merek__iexact=selected_brand)

    # Filter by Harga Minimum
    min_price = request.GET.get('min_price')
    if min_price and min_price != "":
        cars_data = cars_data.filter(harga__gte=min_price)

    # Filter by Harga Maximum
    max_price = request.GET.get('max_price')
    if max_price and max_price != "":
        cars_data = cars_data.filter(harga__lte=max_price)

    # ================= LOGIKA SORTING (PENGURUTAN) =================
    
    sort_by = request.GET.get('sort', 'newest') # Default: newest
    
    if sort_by == 'price_low':
        cars_data = cars_data.order_by('harga')       # Harga Terendah
    elif sort_by == 'price_high':
        cars_data = cars_data.order_by('-harga')      # Harga Tertinggi
    elif sort_by == 'year_new':
        cars_data = cars_data.order_by('-tahun')      # Tahun Muda
    elif sort_by == 'year_old':
        cars_data = cars_data.order_by('tahun')       # Tahun Tua
    else:
        cars_data = cars_data.order_by('-id')         # Default (Input Terakhir)

    # ================= LOGIKA PAGINATION (HALAMAN) =================
    
    items_per_page = request.GET.get('paginate_by', 5)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 5

    paginator = Paginator(cars_data, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ================= DATA PENDUKUNG DROPDOWN =================
    
    # Ambil daftar merek unik yang ada di database untuk opsi Dropdown Filter
    # flat=True membuat hasilnya jadi list ['Honda', 'Toyota', ...] bukan object
    brands_list = Cars.objects.values_list('merek', flat=True).distinct().order_by('merek')

    context = {
        "cars": page_obj,
        "items_per_page": items_per_page,
        "brands_list": brands_list,       # Untuk dropdown merek
        "selected_brand": selected_brand, # Agar filter tidak reset saat ganti halaman
        "min_price": min_price,
        "max_price": max_price,
        "current_sort": sort_by,
    }

    return render(request, "demo/car_list_dashboard.html", context)

def dashboard_customer_list(request):
    if not request.user.is_authenticated:
        return redirect("demo_login")

    # 1. Ambil data awal (urutkan dari terbaru)
    orders_data = Order.objects.select_related("customer", "trade_in_car", "showroom_car").all().order_by('-id')

    # ================= LOGIKA FILTERING =================
    
    # 1. Filter by Nama Customer (Search)
    search_query = request.GET.get('q')
    if search_query and search_query != "":
        orders_data = orders_data.filter(customer__name__icontains=search_query)

    # 2. Filter by Status Customer
    selected_status = request.GET.get('status')
    if selected_status and selected_status != "":
        orders_data = orders_data.filter(customer__status__iexact=selected_status)

    # 3. Filter by Order Type (BARU) 
    # Menggunakan 'offer_type' sesuai nama field di model Order
    selected_type = request.GET.get('type')
    if selected_type and selected_type != "":
        orders_data = orders_data.filter(offer_type__iexact=selected_type)

    # ================= LOGIKA PAGINATION =================
    
    items_per_page = request.GET.get('paginate_by', 5)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 5

    paginator = Paginator(orders_data, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ================= DATA PENDUKUNG DROPDOWN =================
    
    # Ambil list status unik
    status_list = Order.objects.values_list('customer__status', flat=True).distinct().order_by('customer__status')
    
    # Ambil list offer_type unik (Buy, Sell, Trade)
    type_list = Order.objects.values_list('offer_type', flat=True).distinct().order_by('offer_type')

    context = {
        'orders': page_obj,
        'items_per_page': items_per_page,
        
        # Data untuk Filter Status
        'status_list': status_list,
        'selected_status': selected_status,
        
        # Data untuk Filter Order Type (BARU)
        'type_list': type_list,
        'selected_type': selected_type,

        'search_query': search_query,
    }

    return render(request, 'demo/customer_list_dashboard.html', context)


# ==================> Demo API
def demo_api(request):

    return render(request,'demo/api/demo_api.html')