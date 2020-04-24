from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('country', views.index, name='country'),
    path('contact', views.contact, name='contact'),
    path('email', views.email, name='mail'),

]