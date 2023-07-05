from django import forms
from .models import Expense, Income, Email, Profile, Category


#  Form for each Expense to be add

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount']
        labels = {
            'amount': 'Amount',
        }


#  Form for the Email to where account summary should be sent
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['username', 'email_id']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile  # Assuming your User model is named User
        fields = ('username', 'bio', 'email', 'phone_number', 'profile_picture')


#
class CategoryForms(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
