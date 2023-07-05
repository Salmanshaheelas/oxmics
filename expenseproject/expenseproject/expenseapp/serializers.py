# serializers.py

# from rest_framework import serializers
# from .models import Expense
#
#
# class ExpenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Expense
#         fields = ['id', 'category', 'amount', 'description', 'date', 'user']

from rest_framework import serializers
from .models import Expense


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

