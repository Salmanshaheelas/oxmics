from django.urls import path
from . import views

app_name = 'expenseapp'

urlpatterns = [
    path('', views.expense_list, name="expense_list"),
    path('create/', views.expense_create, name="expense_create"),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('update/<int:pk>/', views.expense_update, name="expense_update"),
    path('delete/<int:pk>/', views.expense_delete, name="expense_delete"),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('send_monthly_summary/', views.send_monthly_summary, name='send_monthly_summary'),
]
