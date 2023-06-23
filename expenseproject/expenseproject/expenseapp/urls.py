from django.urls import path
from . import views


urlpatterns = [
    path('', views.expense_list, name="expense-list"),
    path('create/', views.expense_create, name="expense_create"),
    path('update/<int:pk>/', views.expense_update, name="expense_update"),
    path('delete/<int:pk>/', views.expense_delete, name="expense_delete"),
    path('send_mail_view', views.send_mail_view, name='send_mail_view'),
]
