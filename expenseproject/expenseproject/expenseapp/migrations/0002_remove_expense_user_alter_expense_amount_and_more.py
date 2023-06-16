# Generated by Django 4.1.3 on 2023-06-13 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenseapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="user",
        ),
        migrations.AlterField(
            model_name="expense",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("food", "Food"),
                    ("transportation", "Transportation"),
                    ("utilities", "Utilities"),
                    ("other", "Other"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name="ExpenseCategory",
        ),
    ]