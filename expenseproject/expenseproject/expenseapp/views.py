from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import ExpenseForm


# Create your views here.

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, "expense_list.html", {'expenses': expenses})

def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "expense_form.html", {'form': form})

def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request, 'expense_detail.html', {'expense': expense})

def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expense_form.html", {'form': form})

def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect("expense_list")
    return render(request, "expense_confirm_delete.html", {'expense': expense})

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
#
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration successful. You can now log in.')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('expense_list')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'login.html')
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('login')

# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserChangeForm
#
# @permission_required('auth.view_user')
# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'user_list.html', {'users': users})
#
# @permission_required('auth.view_user')
# def user_detail(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     return render(request, 'user_detail.html', {'user': user})
#
# @permission_required('auth.change_user')
# def user_update(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_detail', user_id=user_id)
#     else:
#         form = UserChangeForm(instance=user)
#     return render(request, 'user_form.html', {'form': form})
#
# @permission_required('auth.delete_user')
# def user_delete(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'user_confirm_delete.html', {'user': user})

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime, timedelta

def send_monthly_summary(request):
    current_date = datetime.now()
    last_month_start = datetime(current_date.year, current_date.month - 1, 1)
    last_month_end = datetime(current_date.year, current_date.month - 1, 1) + timedelta(days=32)

    expenses = Expense.objects.filter(user=request.user, date__range=(last_month_start, last_month_end))

    # Calculate total expenses for the month
    total_expenses = sum(expense.amount for expense in expenses)

    # Render the email template with the expenses and total
    email_subject = f"Monthly Account Summary - {last_month_start.strftime('%B %Y')}"
    email_body = render_to_string('email/monthly_summary.html', {'expenses': expenses, 'total_expenses': total_expenses})

    # Send the email
    email = EmailMessage(email_subject, email_body, to=[request.user.email])
    email.send()

    return redirect('expense_list')



import calendar
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_monthly_summary(request):
    now = datetime.now()
    month = now.month
    year = now.year
    last_day = calendar.monthrange(year, month)[1]
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, last_day)
    expenses = Expense.objects.filter(user=request.user.profile.username, date__range=[start_date, end_date])
    summary_data = calculate_summary(expenses)
    email = request.user.profile.email
    send_account_summary_email(email, calendar.month_name[month], year, summary_data)

def send_account_summary_email(email, month, year, summary_data):
    subject = f"Account Summary for {month} {year}"
    html_content = render_to_string('expenses/account_summary_email.html', {'summary_data': summary_data})
    email_message = EmailMessage(subject, html_content, to=[email])
    email_message.content_subtype = 'html'
    email_message.send()


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


# import datetime
# from django.core.mail import send_mail
# from django.shortcuts import render
# from django.conf import settings
# from django.template.loader import render_to_string
#
# today = datetime.date.today()
# weekday = today.weekday()
#
#
# def send_mm_email(request):
#     template = render_to_string('account_summary_email.html', {'name': request.user.profile.username})
#
#     if (weekday == 4):
#         email = send_mail(
#             "Monthly Account Summary",
#             template,
#             settings.EMAIL_HOST_USER,
#             [request.user.profile.email],
#         )
#         print('Friday, mails sent')
#
#     else:
#         print('Not Friday')
#
#     email.fail_silently = False
#     email.send()
#
#     expense = Expense.objects.all()
#     context = {'expense': expense}
#
#     return render(request, 'account_summary_email.html', context)