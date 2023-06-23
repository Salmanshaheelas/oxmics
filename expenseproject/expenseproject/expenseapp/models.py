from django.db import models

# Create your models here.

# Models for the categories of Expenses
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=250, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

#  Model for the Email to be send in
class Email(models.Model):
    username = models.CharField(max_length=250)
    email_id = models.EmailField(max_length=250)

