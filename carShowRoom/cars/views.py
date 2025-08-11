from django.shortcuts import render

# Create your views here.
def carList(request):

    return render(request,'cars/index.html')