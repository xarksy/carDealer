from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from cars.models import Cars
from customer.models import Customer
from .forms import TradeinForm
from customer.forms import CustomerForm
import logging

logger = logging.getLogger(__name__)

def placing_order_view(request):
    # Ambil parameter action dari GET (URL) atau POST (Form) agar konsisten
    action = request.GET.get("action") or request.POST.get("action")
    car_id = request.GET.get("car_id") or request.POST.get("car_id")
    
    car = get_object_or_404(Cars, id=car_id) if car_id else None
    
    # Inisialisasi Form
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        trade_form = TradeinForm(request.POST)
        
        if action == "Trade":
            # Untuk Trade-in, WAJIB validasi kedua form
            if trade_form.is_valid() and customer_form.is_valid():
                customer = customer_form.save()
                
                # Simpan data Trade In
                trade_in_car = trade_form.save(commit=False)
                trade_in_car.customer = customer
                trade_in_car.save()
                
                # Buat Order Utama
                order = Order(
                    customer=customer, 
                    offer_type="trade",
                    showroom_car=car,
                    trade_in_car=trade_in_car
                )
                order.save()

                # === TAMBAHKAN KODE INI ===
                # Update status mobil menjadi Sold atau Booked
                if car:
                    car.status = 'sold' # Pastikan field 'status' ada di models.py app Cars
                    car.save()
                # ==========================
                
                # 2. TAMBAHKAN PESAN SUKSES DI SINI
                messages.success(request, "Data sudah disimpan, tim kami segera menghubungi anda.")

                return redirect('detail_car', car_id=car.id)
            else:
                logger.error("Trade Error: %s %s", customer_form.errors, trade_form.errors)
                messages.error(request, "Mohon periksa kembali data yang Anda masukkan.") # Opsional: Pesan error

        elif action == "Buy":
            # Untuk Buy, HANYA validasi customer_form (trade_form diabaikan)
            if customer_form.is_valid():
                customer = customer_form.save()
                
                # Buat Order Utama
                order = Order(
                    customer=customer, 
                    offer_type="buy",
                    showroom_car=car
                )
                order.save()

                # === TAMBAHKAN KODE INI ===
                # Update status mobil menjadi Sold atau Booked
                if car:
                    car.status = 'sold' # Pastikan field 'status' ada di models.py app Cars
                    car.save()
                # ==========================

                # 3. TAMBAHKAN PESAN SUKSES DI SINI
                messages.success(request, "Data sudah disimpan, tim kami segera menghubungi anda.")
                
                return redirect('detail_car', car_id=car.id)
            else:
                logger.error("Buy Error: %s", customer_form.errors)

                messages.error(request, "Mohon periksa kembali data yang Anda masukkan.") # Opsional: Pesan error
    
    else:
        # Method GET: Tampilkan form kosong
        customer_form = CustomerForm()
        trade_form = TradeinForm()

    context = {
        "customer_form": customer_form,
        "trade_form": trade_form, # Variabel ini yang dikirim ke template
        "action": action,
        "car_id": car_id,
        "car": car # Tambahkan object car agar bisa menampilkan info mobil di header (opsional)
    }

    return render(request, 'orders/order_form.html', context)