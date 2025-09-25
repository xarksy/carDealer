from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import User
from cars.views import admin_required
import logging
logger = logging.getLogger(__name__)

@admin_required
def userView(request):

    return render(request,'base.html')

@admin_required
def userlist_view(request):

    context = {
        'users' : User.objects.all()
    }

    return render(request,'users/user_index.html',context)

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