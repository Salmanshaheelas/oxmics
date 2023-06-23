from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import ExpenseForm, EmailForm
from django.utils import timezone
import calendar
from django.core.mail import send_mail


# Create your views here.


# View to the main page where we can list our new expenses
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, "expense_list.html", {'expenses': expenses})


# view to the form to create a new expense
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "expense_form.html", {'form': form})


#  View to update an expense
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense-list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expense_form.html", {'form': form})


# View to delete an expense
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect("expense-list")
    return render(request, "expense_confirm_delete.html", {'expense': expense})


# View to send mail to user on the monthly account summary
def send_mail_view(request):
    now = timezone.now()
    month = now.month
    year = now.year
    last_day = calendar.monthrange(year, month)[1]
    start_date = timezone.datetime(year, month, 1)
    end_date = timezone.datetime(year, month, last_day)
    expenses = Expense.objects.all()
    summary_data = calculate_summary(expenses)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f" This is your monthly account summary starting from{start_date} and upto {end_date}"
            message = f" This Email shows your expenses of last month based on using the expense tracker app and hence we are showing the expense summary between {start_date} to {end_date} and the details about the expense on last month is \n {summary_data}"
            send_mail(subject, message, "salmanshaheelas@gmail.com", [cd['email_id']])
            return redirect("expense-list")
        else:
            print("Form not valid")
    else:
        form = EmailForm()
    return render(request, "account_summary_email.html", {'form': form})


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
