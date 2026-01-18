from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import UserLog

@login_required
def dashboard_log(request):
    # 1. Keamanan: Hanya admin yang boleh lihat log
    if request.user.role != 'admin':
        return redirect('demo_dashboard')
    
    # 2. Ambil data log (terbaru diatas)
    logs_data = UserLog.objects.select_related('user').all().order_by('-id')

    # =========== FILTERING ============

    # Filter by User (Search Username)
    search_user = request.GET.get('q')
    if search_user:
        logs_data = logs_data.filter(user__username__icontains=search_user)
    
    # Filter by Action (Create/Update/Delete)
    selected_action = request.GET.get('action')
    if selected_action:
        logs_data = logs_data.filter(action__iexact=selected_action)
    
    # =========== PAGINATION ============

    items_per_page = request.GET.get('paginate_by', 10) # Defautl 10
    try :
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    paginator = Paginator(logs_data, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Data pendukung untuk dropdown filter
    action_list = ['CREATE',
                   'UPDATE',
                   'DELETE',
                   'LOGIN',
                   'LOGOUT']
    
    context = {
        'logs' : page_obj,
        'items_per_page' : items_per_page,
        'search_user' : search_user,
        'selected_action' : selected_action,
        'action_list' : action_list
    }

    return render(request, 'activity_log/log_list.html', context)

# Create your views here.
