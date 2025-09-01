from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
def userView(request):

    return render(request,'base.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form':form})

def userlist_view(request):

    context = {
        'users' : User.objects.all()
    }

    return render(request,'users/user_index.html',context)

