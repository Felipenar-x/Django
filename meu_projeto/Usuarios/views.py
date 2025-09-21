from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Product


# Create your views here.
def Registro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/registro.html')


    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('password_confirm', '')


    if not username or not email or not password:
        messages.error(request, 'Todos os campos são obrigatórios.')
        return render(request, 'usuarios/registro.html', {'username': username, 'email': email})

    if password != password_confirm:
        messages.error(request, 'As senhas não coincidem.')
        return render(request, 'usuarios/registro.html', {'username': username, 'email': email})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe.')
        return render(request, 'usuarios/registro.html', {'username': username, 'email': email})

    try:
        User.objects.create_user(username=username, email=email, password=password)
    except Exception as e:
        messages.error(request, f'Erro ao criar usuário: {e}')
        return render(request, 'usuarios/registro.html', {'username': username, 'email': email})

    messages.success(request, 'Registrado com sucesso. Faça login.')
    return redirect('Usuarios:login')


def Login(request):
    if request.method == 'GET':
        # consume any existing messages so they don't appear on the login page later
        list(messages.get_messages(request))
        return render(request, 'usuarios/login.html')


    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        messages.success(request, 'Login realizado com sucesso.')
        return redirect('Homepage')
    else:
        messages.error(request, 'Credenciais inválidas.')
        return render(request, 'usuarios/login.html', {'username': username})


def Logout(request):
    auth_logout(request)
    messages.info(request, 'Você saiu.')
    return redirect('inicial')


@login_required(login_url='Usuarios:login')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        quantity = request.POST.get('quantity', '1')
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except Exception:
            quantity = 1

        if not name:
            messages.error(request, 'Nome do produto é obrigatório.')
            return redirect('Homepage')

        product, created = Product.objects.get_or_create(owner=request.user, name__iexact=name, defaults={'name': name, 'quantity': quantity})
        if not created:
            product.quantity = product.quantity + quantity
            product.save()
        messages.success(request, f'Produto "{name}" adicionado.')

    return redirect('Homepage')


@login_required(login_url='Usuarios:login')
def remove_product(request):
    """Remove a product from the DB by product id (POST 'product_id')."""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id, owner=request.user)
            product_name = product.name
            product.delete()
            messages.success(request, f'Produto "{product_name}" removido.')
        except Product.DoesNotExist:
            messages.error(request, 'Produto não encontrado.')
        except Exception:
            messages.error(request, 'Erro ao remover produto.')

    return redirect('Homepage')