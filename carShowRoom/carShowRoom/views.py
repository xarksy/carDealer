from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('carList')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('carList')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login_form.html')

def logout_view(request):
    logout(request)
    return redirect("login")

def api_login(request):
    return render(request,'api_login.html')