import smtplib
from ldevcatalyst import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import SupportRequest
import yaml
from cerberus import Validator

@require_POST
def support_form_submit(request):
    if request.method == 'POST':
        # Assuming you're receiving form data in the request.POST dictionary
        # Extract form data
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        account_role = request.POST.get('account_role')
        support_category = request.POST.get('support_category')
        short_description = request.POST.get('short_description')
        request_schema='''
        name:
            type: string
            required: true

        csrfmiddlewaretoken:
            type: string
            required: true

        email:
            type: string
            required: true
            regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        mobile:
            type: string
            required: true
            regex: '^\d{10}$'

        account_role:
            type: string
            required: true
        
        support_category:
            type: string
            required: true
        
        short_description:
            type: string
            required: true
        
        '''
        v=Validator()
        post_data = request.POST.dict()
        schema=yaml.load(request_schema, Loader=yaml.SafeLoader)     
        if v.validate(post_data,schema):
            # Save form data to the database
            create_support = SupportRequest.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                account_role=account_role,
                support_category=support_category,
                short_description=short_description
            )
            create_support.save()

            # Sending email notification
            try:
                # SMTP Configuration
                email_host = settings.email_host
                email_port = settings.email_port
                email_username = settings.email_username
                email_password = settings.email_password
                email_from = settings.email_from
                email_to = [
                    'support@ldev.in',
                    'itsupport@tnthub.org',
                    'Developer@tnthub.org'
                ]

                # Email content
                subject = 'New Support Request'
                body = f'''
                        Name: {name}
                        email: {email}
                        mobile: {mobile}
                        Account Role: {account_role}
                        Support Category: {support_category}
                        Short Description: {short_description}
                        '''
                # Constructing email message
                message = MIMEMultipart()
                message['From'] = 'aso.itnt@tn.gov.in'
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                # Send email
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    server.login(email_username, email_password)
                    server.sendmail(email_from, email_to, message.as_string())
                
                return JsonResponse({'success': True,'email_status' : False})
            except Exception as e:
                return JsonResponse({'success': True,'email_status' : False})
        else:
            return JsonResponse(
                    {
                        'success': False,
                        'registration_id': "Failed",
                        'error': v.errors,
                    })
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request method'})
