# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
#
# from . import views
# from djoser.views import TokenCreateView
#
# urlpatterns = [
#     path('<int:pk>', views.expense_list, name="expense-list"),

# #
# #     path('api/expenses/', views.ExpenseListCreateView.as_view(), name='expense_list_create'),
# #     path('api/expenses/<int:pk>/', views.ExpenseRetrieveUpdateDestroyView.as_view(), name='expense_detail'),
# #     path('auth/token/', TokenCreateView.as_view(), name='token_create'),
# #     path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# #     path('create/', views.expense_create, name="expense_create"),
# #     path('update/<int:pk>/', views.expense_update, name="expense_update"),
# #     path('delete/<int:pk>/', views.expense_delete, name="expense_delete"),
# #     path('send_mail_view', views.send_mail_view, name='send_mail_view'),
# ]

from django.urls import include, path
from rest_framework import routers
from .views import ExpenseViewSet, ReactView
from . import views
router = routers.DefaultRouter()
# router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('create-expense/', views.create_expense, name='create_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('expense/update/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('expense/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('user/settings/', views.user_settings, name='user_settings'),
    path('send_mail_view', views.send_mail_view, name='send_mail_view'),
    path('wel/', ReactView.as_view(), name="something")
]
