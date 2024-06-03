from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(subject,text_content,user,html_content):
    """
        send mail 
        
            Arguments:
                subject, text_content,user,html_content

    """
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user.email,]
    recipient_list = ['shivahir0114@gmail.com',]
    email=EmailMultiAlternatives(subject,text_content,email_from,recipient_list)
    email.attach_alternative(html_content,'text/html')
    email.send()

