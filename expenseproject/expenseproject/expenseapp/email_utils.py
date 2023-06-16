# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
#
# def send_account_summary_email(email, month, year, summary_data):
#     subject = f"Account Summary for {month} {year}"
#     html_content = render_to_string('account_summary_email.html', {'summary_data': summary_data})
#     email_message = EmailMessage(subject, html_content, to=[email])
#     email_message.content_subtype = 'html'
#     email_message.send()
