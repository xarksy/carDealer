from django.shortcuts import render

# Create your views here.
def userView(request):

    return render(request,'base.html')