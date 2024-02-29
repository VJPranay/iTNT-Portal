from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

# message = get_template("emails/student_invite.html").render({
#                     'registration_url': registration_url
#                 })
from_email = settings.EMAIL_HOST_FROM
mail = EmailMultiAlternatives(
                    "Test email",
                    "This is a test email",
                    from_email=from_email,
                    to=['pranaymadasi1@gmail.com'],
                )
mail.content_subtype = "html"
mail.mixed_subtype = 'related'
mail.attach_alternative("This is a test email", "text/html")
send = mail.send()