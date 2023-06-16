from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import ExpenseForm
# import calendar
# from datetime import datetime
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
from django.contrib.auth import get_user_model



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


# def send_monthly_summary(user):
#     def calculate_summary(expenses):
#         total_expenses = 0
#         for expense in expenses:
#             total_expenses += expense.amount
#
#         average_daily_expense = total_expenses / len(expenses)
#
#         return {
#             'expenses': expenses,
#             'total_expenses': total_expenses,
#             'average_daily_expense': average_daily_expense,
#         }
#
#     now = datetime.now()
#     month = now.month
#     year = now.year
#     last_day = calendar.monthrange(year, month)[1]
#     start_date = datetime(year, month, 1)
#     end_date = datetime(year, month, last_day)
#     expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])
#     summary_data = calculate_summary(expenses)
#
#     email = user.email
#     send_account_summary_email(email, calendar.month_name[month], year, summary_data)
#
#
# def send_account_summary_email(email, month, year, summary_data):
#     subject = f"Account Summary for {month} {year}"
#     html_content = render_to_string('expenses/account_summary_email.html', {'summary_data': summary_data})
#     email_message = EmailMessage(subject, html_content, to=[email])
#     email_message.content_subtype = 'html'
#     email_message.send()


