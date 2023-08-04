from django.urls import path, include
from djoser.urls import authtoken
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ExpenseViewSet, IncomeViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'incomes', IncomeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include(authtoken)),
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'}), name='user-register'),

    
]
