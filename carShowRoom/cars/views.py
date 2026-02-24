from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars, CarImage
from .forms import CarsForm, ServiceHistoryForm
from django.http import HttpResponseForbidden
from customer.forms import CustomerForm
from orders.forms import TradeinForm
from orders.models import Order
from customer.models import Customer
from django.db.models import Sum, Count
from activity_log.utils import log_activity

import logging
logger = logging.getLogger(__name__)


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role in ["admin"]):
            return view_func(request, *args, **kwargs)
        # return HttpResponseForbidden("Not allowed")
        return redirect("carList")

    return wrapper

def carList(request):
    print(request.user)

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST or None)
        trade_form = TradeinForm(request.POST or None)

        if customer_form.is_valid() and trade_form.is_valid():
            customer = customer_form.save()
            order = Order(customer=customer, offer_type="sell") 
            placing_order = trade_form.save(commit=False)
            placing_order.customer = customer
            placing_order.save()
            order.trade_in_car = placing_order
            
            order.save()
            return redirect('success_page')
        else:
            logger.error("Form submission failed with errors: %s", {"customer_form": customer_form.errors, "trade_form": trade_form.errors})

    else:
        customer_form = CustomerForm()
        trade_form = TradeinForm()

    cars_data = Cars.objects.order_by('-id').filter(status='available')

    context = {
        'cars' : cars_data,
        "customer_form": customer_form,
        "trade_form": trade_form,
    }

    return render(request,'cars/index.html',context)

# ====================== CRUD CAR
@admin_required
def create_car(request):
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        
        # --- TAMBAHAN MULTIPLE UPLOAD ---
        gallery_images = request.FILES.getlist('gallery_images')
        main_index = int(request.POST.get('main_image_index', 0))
        # --------------------------------

        if form.is_valid():
            created_car = form.save(commit=False) # Tahan dulu, jangan disave ke DB
            
            # Set gambar utama jika ada yang diupload
            if gallery_images and main_index < len(gallery_images):
                created_car.gambar = gallery_images[main_index]
            
            created_car.save() # Sekarang simpan ke DB

            # Simpan sisa gambar ke galeri (CarImage)
            if gallery_images:
                for i, img in enumerate(gallery_images):
                    if i != main_index:
                        CarImage.objects.create(mobil=created_car, image=img)

            # === LOGGING (Asli milik Anda) ===
            log_activity(
                user=request.user, 
                action='CREATE', 
                target_model='Mobil', 
                description=f"Menambahkan mobil {created_car.nama} ({created_car.merek})"
            )
            # ==================================

            next_url = request.GET.get('next', 'carList')
            return redirect(next_url)
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CarsForm()
    
    context = {
        'form': form
    }

    return render(request,'cars/car_form.html',context)


def updateCar(request, car_id):
    """
    View to update the details of a specific car.
    """
    car = get_object_or_404(Cars, id=car_id)
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES, instance=car)
        
        # --- TAMBAHAN MULTIPLE UPLOAD ---
        gallery_images = request.FILES.getlist('gallery_images')
        main_index = int(request.POST.get('main_image_index', 0))
        # --------------------------------

        if form.is_valid():
            updated_car = form.save(commit=False)

            # Timpa gambar utama HANYA jika ada gambar baru yang diupload
            if gallery_images and main_index < len(gallery_images):
                updated_car.gambar = gallery_images[main_index]
            
            updated_car.save()

            # Tambahkan gambar baru ke galeri (CarImage) jika ada
            if gallery_images:
                for i, img in enumerate(gallery_images):
                    if i != main_index:
                        CarImage.objects.create(mobil=updated_car, image=img)

            # === LOGGING (Asli milik Anda) ===
            log_activity(
                user=request.user, 
                action='UPDATE', 
                target_model='Mobil', 
                description=f"Update mobil {updated_car.nama} ({updated_car.merek})"
            )
            # ==================================

            next_url = request.GET.get('next', 'carList')
            return redirect(next_url)
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CarsForm(instance=car)
    
    context = {
        'form': form,
        'car': car # Lempar object car agar bisa mengecek gambar lama di template HTML
    }

    return render(request, 'cars/car_form.html',context=context)

@admin_required
def deleteCar(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    car.delete()

    # === TAMBAHKAN INI SETELAH SAVE ===
    log_activity(
        user=request.user, 
        action='DELETE', 
        target_model='Mobil', 
        description=f"Menghapus mobil {car.nama} ({car.merek})"
    )
    # ==================================

    # return redirect('carList')
    next_url = request.GET.get('next', 'carList')
    return redirect(next_url)

def detail_car(request, car_id):

    car = get_object_or_404(Cars, id=car_id)
    service_history = car.service_histories.all()
    total_biaya = sum(service.biaya for service in service_history)    

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save()
            order = Order(customer=customer, offer_type="buy")
            order.showroom_car = car
            order.save()
            # form.save()
            return redirect('carList')
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CustomerForm()

    context = {
        'car': car,
        'service_history': service_history,
        'total_biaya': total_biaya,
        'cash': total_biaya + car.harga,
        'trade_in_forms': form
    }

    return render(request, 'cars/detail.html', context)

# ===== CRUD CAR SERVICE
@admin_required
def car_service_plain(request):
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carList')
            
    else:
        form = ServiceHistoryForm()
    
    context = {
        'form' : form
    }

    return render(request, 'cars/service_history_form.html', context=context)

@admin_required
def car_service(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST, request.FILES, hide_car_field=True)
        if form.is_valid():
            service_history = form.save(commit=False)
            service_history.car = car
            service_history.save()

            # === LOGGING ===
            log_activity(
                user=request.user,
                action='UPDATE', # Atau 'CREATE' karena ini menambah data servis baru
                target_model='Service History',
                # Gunakan variabel 'car' langsung karena 'service_history' adalah anak dari 'car'
                description=f"Menambah data servis untuk mobil {car.nama} ({car.merek})"
            )
            # ===============
            
            return redirect('detail_car',car_id=car.id)
    else:
        form = ServiceHistoryForm(initial={'mobil': car.id}, hide_car_field=True)
    
    context = {
        'form' : form,
        'car' : car
    }

    return render(request,'cars/service_history_form.html', context=context)

#=============== success page
def success_page(request):

    return render(request, 'cars/success_page.html')