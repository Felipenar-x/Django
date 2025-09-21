from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Usuarios.models import Product


@login_required(login_url='Usuarios:login')
def Homepage(request):
    products = Product.objects.filter(owner=request.user).order_by('-id')
    return render(request,'home/homepage.html', {'products': products})

def Default(request):
    return render(request,'home/default.html')