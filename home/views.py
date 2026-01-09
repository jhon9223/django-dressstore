from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import category, product
from django.contrib.auth.models import User, auth
from .forms import ProductForm, categoryform, editproductform
# Create your views here.


def home(request):
    x = category.objects.all()
    y = product.objects.all()
    return render(request, 'home.html', {'prod': y, 'cat': x})


def view_product(request, pid):
    x = product.objects.get(id=pid)
    return render(request, 'product.html', {'prod': x})


def view_category(request, cid):
    x = product.objects.filter(cat=cid)
    return render(request, 'category.html', {'prod': x})


def register_fn(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'msg': 'user already exists'})
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=fname,
                    last_name=lname
                )

                return redirect('/')
        else:
            return render(request, 'register.html', {'msg': 'password not matching'})
    return render(request, 'register.html')


def login_fn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/home')
        else:
            return render(request, 'login.html', {'msg': 'invalid credentials'})
    return render(request, 'login.html')


def logout_fn(request):
    auth.logout(request)
    return redirect('/')


def add_product(request):
    if request.method == "POST":
        f = ProductForm(request.POST, request.FILES)
        if f.is_valid():
            x = f.save(commit=False)
            x.us = request.user
            x.save()
            return redirect('/home')
    else:
        f = ProductForm()
        return render(request, 'add_product.html', {'fm': f})


def edit_product(request, pid):
    if request.method == "POST":
        x = product.objects.get(id=pid)
        f = editproductform(request.POST, request.FILES, instance=x)
        if f.is_valid():
            f.save()
            return redirect('/home')
    else:
        x = product.objects.get(id=pid)
        f = editproductform(instance=x)
        return render(request, 'edit_product.html', {'fm': f})


def delete_product(request, pid):
    x = product.objects.get(id=pid)
    x.delete()
    return redirect('/home')
