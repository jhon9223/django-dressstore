"""
URL configuration for Dressstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('view_category/<int:cid>', view_category, name='view_category'),
    path('view_product/<int:pid>', view_product, name='view_product'),
    path('register/', register_fn, name='register'),
    path('', login_fn, name='login'),
    path('logout/', logout_fn, name='logout'),
    path('add_product/', add_product, name='add_product'),
    path("editproduct/<int:pid>", edit_product, name="editproduct"),
    path("deleteproduct/<int:pid>", delete_product, name="deleteproduct"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
