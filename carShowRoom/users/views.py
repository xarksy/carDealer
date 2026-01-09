from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import User
from cars.views import admin_required
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

@admin_required
def userView(request):

    return render(request,'base.html')

@admin_required
def userlist_view(request):
    # 1. Cek Login & Permission (Hanya Admin yang boleh lihat user list)
    if not request.user.is_authenticated:
        return redirect("demo_login")
    
    # Opsional: Jika Anda ingin membatasi halaman ini hanya untuk admin
    # if request.user.role != 'admin':
    #     return redirect("demo_dashboard")

    # 2. Ambil semua data User (Urutkan dari yang terbaru)
    users_data = User.objects.all().order_by('-id')

    # ================= LOGIKA FILTERING =================
    
    # Filter by Role (Sesuai permintaan)
    selected_role = request.GET.get('role')
    if selected_role and selected_role != "":
        users_data = users_data.filter(role__iexact=selected_role)

    # ================= LOGIKA PAGINATION =================
    
    items_per_page = request.GET.get('paginate_by', 5)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 5

    paginator = Paginator(users_data, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ================= DATA PENDUKUNG =================
    
    # Ambil daftar Role unik yang ada di database untuk dropdown
    roles_list = User.objects.values_list('role', flat=True).distinct().order_by('role')

    context = {
        'users': page_obj,
        'items_per_page': items_per_page,
        'roles_list': roles_list,        # Untuk dropdown filter role
        'selected_role': selected_role,  # Agar filter tidak reset
    }

    return render(request, 'demo/userlist_dashboard.html', context)

@admin_required
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form':form})

@admin_required
def update_user_view(request, user_id):
    """
    View to update the details of a specific car.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            logger.error("Form submission failed: %s", form.errors)
    else:
        form = CustomUserCreationForm(instance=user)
    
    context = {
        'form': form
    }

    return render(request, 'users/register.html',context=context)

@admin_required
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()

    return redirect('user_list')