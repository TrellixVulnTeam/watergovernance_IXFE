"""watergovernance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from water import views

urlpatterns = [
    path('',views.index),
    path('signup',views.signup),
    path('signin_admin',views.signinadmin),
    path('signin_user',views.signin_user),
    path('aboutUs',views.aboutUs),
    path('contact',views.contact),
<<<<<<< HEAD
    path('admin/',views.adminland)
=======
    path('admin',views.adminland),
    path('user',views.userland),
    path('adminModel',views.modelResult)
>>>>>>> 21e0313a3d60d12a4882ce79b05118748b46b0d4
]
