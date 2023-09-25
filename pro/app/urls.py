from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.signin,name='contact'),
    path("register",views.register,name="register"),
    path('contact',views.contact,name='contact'),
    path("signin",views.signin,name="signin"),
    path('display',views.display,name="display"),
    #path('update/<str:id>',views.update,name="update"),
    path('delete/<str:id>',views.delete,name="delete") ,
    path('search',views.search,name="search"),
    path('home',views.home,name="home"),]