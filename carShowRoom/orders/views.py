from django.shortcuts import render

# Create your views here.
def placing_order_view(request):

    return render(request,'orders/order_form.html')