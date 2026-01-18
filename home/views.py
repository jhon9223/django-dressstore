from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import category, product, profile
from django.contrib.auth.models import User, auth
from .forms import ProductForm, categoryform, editproductform, profileform
from django.contrib.auth.decorators import login_required
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


def themecookie(request):
    m = request.COOKIES.get("theme", "light")
    if m == "light":
        m = "dark"
    else:
        m = "light"
    r = redirect('/home')
    r.set_cookie("theme", m)
    return r


# def themesession(request):
#     m = request.COOKIES.get("theme", "light")
#     if m == "light":
#         m = "dark"
#     else:
#         m = "light"

#     request.session['theme'] = m
#     return redirect('/home')
def themesession(request):
    theme = request.session.get("theme", "light")

    if theme == "light":
        theme = "dark"
    else:
        theme = "light"

    request.session["theme"] = theme
    return redirect("/home")


def home(request):
    if request.user.username:
        x = category.objects.all()
        y = product.objects.all()
        # r = render(request, 'home.html', {'prod': y, 'cat': x})
        # r.set_cookie("abc", "123")
        # return r
        # m = request.COOKIES.get("theme", "light")
        m = request.session.get("theme", "light")
        return render(request, 'home.html', {'prod': y, 'cat': x, 'theme': m})
    else:
        return redirect('/welcome')


@login_required(login_url='/welcome')
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
    return redirect('/welcome')


@login_required(login_url='/welcome')
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
            x = f.save(commit=False)
            x.us = request.user
            x.save()
            return redirect('/home')
    else:
        x = product.objects.get(id=pid)
        f = editproductform(instance=x)
        return render(request, 'edit_product.html', {'fm': f})


def delete_product(request, pid):
    x = product.objects.get(id=pid)
    x.delete()
    return redirect('/home')


@login_required(login_url='/welcome')
def profilefn(request):
    if profile.objects.filter(us=request.user).exists():
        pro = product.objects.filter(us=request.user)
        a = request.COOKIES.get("abc")
        print(a)
        return render(request, 'profile.html', {'prod': pro})
    else:
        return redirect('/addprofile')


def welcome_fn(request):

    return render(request, 'welcome.html')


def about_us(request):
    x = category.objects.all()
    y = product.objects.all()
    return render(request, 'about.html', {'prod': y, 'cat': x})


def addprofile_fn(request):
    if request.method == "POST":
        f = profileform(request.POST, request.FILES)
        if f.is_valid():
            x = f.save(commit=False)
            x.us = request.user
            x.save()
            return redirect('/profile')
    else:
        f = profileform()
    return render(request, 'addprofile.html', {'fm': f})


def productapi(request):
    return render(request, 'productapi.html')


@api_view(['GET'])
def ourprodapi(request):
    x = product.objects.all()
    y = ProductSerializer(x, many=True)
    return Response(y.data)


def ourprodapi_view(request):
    return render(request, 'ourprodapi.html')


@api_view(['GET'])
def apiviewproduct(request, pid):
    x = product.objects.get(id=pid)
    y = ProductSerializer(x)
    return Response(y.data)


# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def appiaddproductfn(request):
#     x = ProductSerializer(data=request.data)
#     if x.is_valid():
#         x.save()
#         return Response(x.data)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def appiaddproductfn(request):
    x = ProductSerializer(data=request.data)

    if x.is_valid():
        x.save()
        return Response(
            x.data,
            status=status.HTTP_201_CREATED
        )

    # 🔴 THIS PART WAS MISSING
    return Response(
        x.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def apieditproductfn(request, pid):
    a = product.objects.get(id=pid)
    x = ProductSerializer(data=request.data, instance=a)
    if x.is_valid():
        x.save()
        return Response(x.data)


@api_view(['DELETE'])
def apideleteproductfn(request, pid):
    a = product.objects.get(id=pid)
    a.delete()
    return Response("done")
