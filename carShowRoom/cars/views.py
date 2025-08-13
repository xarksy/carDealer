from django.shortcuts import render
from .models import Cars
# Create your views here.
def carList(request):

    context = {
        'cars' : Cars.objects.all()
    }

    return render(request,'cars/index.html',context)