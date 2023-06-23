from django import forms
from .models import Expense, Email


# Form for each Expense to be add
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']


#  Form for the Email to where account summary should be sent
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['username', 'email_id']
