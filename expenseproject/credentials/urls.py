from django.urls import path
from . import views

app_name = 'credentials'

urlpatterns = [
    path('register', views.register, name='register'),

    ]