from django import forms
from .models import Expense, Income, Email, Profile, Category


#  Form for each Expense to be add

class ExpenseForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select a category')
    # category = forms.ModelChoiceField(queryset=Category.objects.all())


    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     category = cleaned_data.get('category')
    #     new_category = cleaned_data.get('new_category')
    #
    #     if not category and not new_category:
    #         self.add_error('category', 'Please select a category or enter a new one.')
    #
    #     return cleaned_data


#
# class UserSettingsForm(forms.ModelForm):
#     class Meta:
#         model = UserSettings
#         fields = ['email', 'username']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         category = cleaned_data.get('category')
#         new_category = cleaned_data.get('new_category')
#
#         if not category and not new_category:
#             self.add_error('category', 'Please select a category or enter a new one.')
#
#         return cleaned_data


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
        fields = ('username','bio', 'email', 'phone_number', 'profile_picture')
#
class CategoryForms(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)