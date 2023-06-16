# from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django.apps import apps
# from . views import send_monthly_summary
# import schedule
#
# class ExpensesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'expenses'
#
#     def ready(self):
#         post_migrate.connect(schedule_monthly_summary_email, sender=self)
#
# @receiver(post_migrate)
# def schedule_monthly_summary_email(sender,):
#     if sender.name == 'expenses':
#         User = get_user_model()
#         for user in User.objects.all():
#
#             schedule.every().month.do(send_monthly_summary, user).tag('monthly_summary')
#
#
#         expenses_app_config = apps.get_app_config('expenses')
#         expenses_app_config.models_module.get_models()
