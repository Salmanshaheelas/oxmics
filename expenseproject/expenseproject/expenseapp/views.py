# from django.shortcuts import render, get_object_or_404, redirect
# from rest_framework.decorators import api_view
# from .models import Expense
# from .forms import ExpenseForm, EmailForm
# from django.utils import timezone
# import calendar
# from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required

# from rest_framework.permissions import IsAuthenticated
#
#
# # Create your views here.

#
# #  VIew to Log In for a User

#
# #  View to Log Out for a User

#
# # views.py
#
# # from rest_framework import permissions, viewsets
# #
# # class ExpenseViewSet(viewsets.ModelViewSet):
# #     queryset = Expense.objects.all()
# #     serializer_class = ExpenseSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_queryset(self):
# #         user = self.request.user
# #         return Expense.objects.filter(user=user)
#
# # View to the main page where we can list our new expenses
#
# from django.shortcuts import get_object_or_404
# from rest_framework import generics, permissions, viewsets
# from .models import Expense
# from .serializers import ExpenseSerializer
#
#
# class ExpenseListCreateView(generics.ListCreateAPIView):
#     serializer_class = ExpenseSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return Expense.objects.filter(user=user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
# class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ExpenseSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return Expense.objects.filter(user=user)
#
#
# @api_view(['GET'])
# def expense_list(request,user_id):
#     expenses = Expense.objects.filter(id=user_id).first()
#     return render(request, "expense_list.html", {'expenses': expenses})
#
#
# # view to the form to create a new expense
# @login_required
# def expense_create(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("expense-list")
#     else:
#         form = ExpenseForm()
#     return render(request, "expense_form.html", {'form': form})
#
#
# #  View to update an expense
# @login_required
# def expense_update(request, pk):
#     expense = get_object_or_404(Expense, pk=pk)
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             return redirect("expense-list")
#     else:
#         form = ExpenseForm(instance=expense)
#     return render(request, "expense_form.html", {'form': form})
#
#
# # View to delete an expense
# @login_required
# def expense_delete(request, pk):
#     expense = get_object_or_404(Expense, pk=pk)
#     if request.method == 'POST':
#         expense.delete()
#         return redirect("expense-list")
#     return render(request, "expense_confirm_delete.html", {'expense': expense})
#
#
# # View to send mail to user on the monthly account summary
# @login_required
# def send_mail_view(request):
#     now = timezone.now()
#     month = now.month
#     year = now.year
#     last_day = calendar.monthrange(year, month)[1]
#     start_date = timezone.datetime(year, month, 1)
#     end_date = timezone.datetime(year, month, last_day)
#     expenses = Expense.objects.all()
#     summary_data = calculate_summary(expenses)
#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             subject = f" This is your monthly account summary starting from{start_date} and upto {end_date}"
#             message = f" This Email shows your expenses of last month based on using the expense tracker app and hence we are showing the expense summary between {start_date} to {end_date} and the details about the expense on last month is \n {summary_data}"
#             send_mail(subject, message, "salmanshaheelas@gmail.com", [cd['email_id']])
#             return redirect("expense-list")
#         else:
#             print("Form not valid")
#     else:
#         form = EmailForm()
#     return render(request, "account_summary_email.html", {'form': form})
#
#
# #  View to Calculate the Summary
# @login_required
# def calculate_summary(expenses):
#     total_expenses = 0
#     for expense in expenses:
#         total_expenses += expense.amount
#
#     average_daily_expense = total_expenses / len(expenses)
#
#     summary_data = {
#         'expenses': expenses,
#         'total_expenses': total_expenses,
#         'average_daily_expense': average_daily_expense,
#     }
#
#     return summary_data

# from django.shortcuts import render
from rest_framework import viewsets, request
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ExpenseForm, IncomeForm, EmailForm, UserSettingsForm, CategoryForms
from .models import Expense, Income
from .serializers import ExpenseSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from datetime import datetime, timedelta, timezone
import calendar
from django.core.mail import send_mail
from django.utils import timezone

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


def index(request):
    return render(request, 'index.html')

# #  View on registering an User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                token, _ = Token.objects.get_or_create(user=user)
                user.save();
                redirect_url = f'/login/?token={token.key}'

                return redirect(redirect_url)
            return Response(status=400)
        else:
            messages.info(request, "Passwords not matching")
    return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, log in the user
            auth_login(request, user)

            # Retrieve the token from the query parameters
            token_key = request.GET.get('token')

            if token_key:
                # Get the token object using the token key
                try:
                    token = Token.objects.get(key=token_key)
                except Token.DoesNotExist:
                    token = None

                # Use the token as needed in your logic
                if token:
                    # Perform any actions with the token
                    pass

            # Redirect the user to the desired page after login
            return redirect('home')  # Replace 'home' with your actual home page URL name

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required
def home(request):
    user = request.user

    # Retrieve expenses and calculate total expenses
    expenses = Expense.objects.filter(user=user)
    total_expenses = sum(expenses.amount for expenses in expenses)

    # Retrieve incomes and calculate total income
    incomes = Income.objects.filter(user=user)
    total_income = sum(incomes.amount for incomes in incomes)

    # Calculate available balance
    available_balance = total_income - total_expenses

    context = {
        'available_balance': available_balance,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'expenses': expenses,
        'incomes': incomes,
    }

    # current_date = datetime.now()
    # start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # end_date = start_date + timedelta(days=31)
    #
    # expense = Expense.objects.filter(created_at__range=(start_date, end_date), user=request.user)

    return render(request, 'home.html', context)


def create_expense(request):
    if request.method == 'POST':
        if "expense" in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('home')
            else:
                expense_form = ExpenseForm()
        elif "category" in request.POST:
            cat_form = CategoryForms(request.POST)
            if cat_form.is_valid():
                category = cat_form.save(commit=False)
                category.save()
                return redirect('home')
            else:
                cat_form = CategoryForms()
    else:
        expense_form = ExpenseForm()
        cat_form = CategoryForms()
    context = {'expense_form': expense_form, 'cat_form': cat_form}
    return render(request, 'create_expense.html', context)


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Set the user field
            income.save()
            return redirect('home')
    else:
        form = IncomeForm()

    context = {'form': form}
    return render(request, 'add_income.html', context)


def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expense_form.html', {'form': form, 'expense': expense})


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        expense.delete()
        return redirect('home')

    return render(request, 'expense_confirm_delete.html', {'expense': expense})


def user_settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserSettingsForm(instance=request.user)

    return render(request, 'user_settings.html', {'form': form})

# View to send mail to user on the monthly account summary




#  View to Calculate the Summary

def calculate_summary(expenses):
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount

    average_daily_expense = total_expenses / len(expenses)

    summary_data = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'average_daily_expense': average_daily_expense,
    }

    return summary_data


# def save_expenses_to_text_file():
#     current_date = datetime.now()
#     last_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
#     file_name = f"expense_list_{last_month.strftime('%Y_%m')}.txt"
#
#     expenses = Expense.objects.filter(created_at__month=last_month.month)
#
#     with open(file_name, 'w') as f:
#         for expense in expenses:
#             f.write(f"{expense.title}\t{expense.amount}\t{expense.category}\t{expense.created_at}\n")
# import datetime
# def generate_expense_report():
#     # Get the start and end dates of the last month
#     today = datetime.date.today()
#     first_day_of_month = datetime.date(today.year, today.month - 1, 1)
#     last_day_of_month = datetime.date(today.year, today.month, 1) - datetime.timedelta(days=1)
#
#     # Retrieve expenses for the last month
#     expenses = Expense.objects.filter(date__range=(first_day_of_month, last_day_of_month))
#
#     # Generate the text file content
#     report_content = ""
#     for expense in expenses:
#         report_content += f"{expense.category}: {expense.amount}\n"
#
#     # Save the report to a text file
#     file_name = f"expense_report_{last_day_of_month.strftime('%Y-%m')}.txt"
#     with open(file_name, 'w') as file:
#         file.write(report_content)
#
#     return file_name

def send_mail_view(request):
    now = timezone.now()
    month = now.month
    year = now.year
    last_day = calendar.monthrange(year, month)[1]
    start_date = timezone.datetime(year, month, 1)
    end_date = timezone.datetime(year, month, last_day)
    incomes = Income.objects.all()
    total_income = sum(incomes.amount for incomes in incomes)
    expenses = Expense.objects.all()
    total_expenses = sum(expenses.amount for expenses in expenses)
    available_balance = total_income - total_expenses
    report_content = ""
    for expense in expenses:
        report_content += f"{expense.category}: {expense.amount}\n"
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f" This is your monthly account summary starting from{start_date} and upto {end_date}"
            message = f"Dear Customer,\n\nPlease find attached your monthly expense report.\n\nThis report shows on which all categories you have spended during the last month and they are \n\n{report_content}\n\n The total Income is{total_income} \n\n Total Expenses is{total_expenses} \n\n Available Balance is{available_balance}\n\n ThankYou for using our App"
            send_mail(subject, message, "salmanshaheelas@gmail.com", [cd['email_id']])
            return redirect("home")
        else:
            print("Form not valid")
    else:
        form = EmailForm()
    return render(request, "account_summary_email.html", {'form': form})


